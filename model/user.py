import hashlib
import random
import re
import string
import time
from pprint import pprint
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.constants import ALGORITHMS
from pydantic import BaseModel

from app_define import VALID_ROLES
from setting import default_setting
from util.errors import DTError
from model.db_model.user import UserDbModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserModel(BaseModel):
    username: str
    password: str
    salt: str
    role: int
    phone: Optional[str] = None
    name: str
    ctime: float
    mtime: float
    last_login_time: float
    remark: Optional[str] = None
    valid: bool
    deleted: bool
    creator: str


def assert_phone_legal(phone):
    if not re.match(r'^[0-9]{11}$', phone):
        raise DTError(u'用户手机号不合法,要求11位,只包含数字')


def assert_username_legal(username):
    if not re.match(r'^[A-Za-z0-9]{4,20}$', username):
        raise DTError(u'用户名不合法,要求4-20位,只包含小写字母和数字')


def assert_name_legal(name):
    if not re.match(r'^[\u4E00-\u9FA5a-zA-Z0-9]{1,20}$', name):
        raise DTError('姓名不合法,要求1-20个字符,只包含中文,大小写字母,数字')


def assert_role_legal(role):
    if role not in VALID_ROLES:
        raise DTError('权限不合法，详情请联系技术人员')


def hash_pwd(pwd, salt):
    hstr = pwd + '|' + salt
    hstr = hstr.encode('utf8')
    return hashlib.sha1(hstr).hexdigest()[:16]


def gen_salt():
    return ''.join(random.choice(string.ascii_letters) for _ in range(16))


def create(username, pwd, role, name, creator='system', phone='', remark=''):
    # pwd 为 hash(username,pwd)一次加密后的pwd
    # test环境为了方便跳过一次加密

    salt = gen_salt()
    cur_time = time.time()
    user_dict = {
        'username': username,
        'password': hash_pwd(pwd, salt),
        'salt': salt,
        'role': role,
        'phone': phone,
        'name': name,
        'ctime': cur_time,
        'mtime': cur_time,
        'last_login_time': cur_time,
        'remark': remark,
        'valid': True,
        'deleted': False,
        'creator': creator
    }
    user = UserModel(**user_dict)  # 验证结构
    return user


def create_user(username, pwd, role, name, creator='system', phone='', remark=''):
    assert_role_legal(role)
    assert_username_legal(username)
    assert_name_legal(name)
    user = create(username, pwd, role, name, creator, phone, remark)
    user_dict = user.dict()
    UserDbModel.update_user_by_username(username, user_dict, upsert=True)
    return username


def load_user_with_pwd(username, password):
    user_dict = UserDbModel.find_by_username(username)
    um = UserModel(**user_dict)
    password = hash_pwd(password, um.salt)
    if password != um.password:
        raise DTError('{}: 密码错误'.format(username))
    return um


def load_user(username):
    user_dict = UserDbModel.find_by_username(username)
    um = UserModel(**user_dict)
    return um


def get_current_user(token: str=Depends(oauth2_scheme)):
    pyload = jwt.decode(token, key=default_setting.secret_key, algorithms=ALGORITHMS.HS256)
    if 'username' not in pyload:
        raise DTError('token:{} 非法,请重新登陆'.format(token))
    um = load_user(pyload['username'])
    return um
    # um = load_user()