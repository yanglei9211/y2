from typing import Optional, Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from setting import default_setting
from model.user import get_current_user
from app_define import USER_ROLE_DATA, USER_ROLE_USER
from util.errors import DTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 依赖注入,用驼峰命名以示区分


def BaseAuthDepends(token: str = Depends(oauth2_scheme)):
    um = get_current_user(token)
    return um


def DataAuthValidate(token: str = Depends(oauth2_scheme)):
    um = BaseAuthDepends(token)
    if not um.role & USER_ROLE_DATA:
        raise DTError("username: {} 没有查看资源的权限".format(um.username))
    return um


def UserAuthValidate(token: str = Depends(oauth2_scheme)):
    um = BaseAuthDepends(token)
    if not um.role & USER_ROLE_USER:
        raise DTError("username: {} 没有查看账号的权限".format(um.username))
    return um
