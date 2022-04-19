import os
import sys
sys.path.append(os.path.abspath("."))
from model.db_model.mongodb import setup_mongodb_client
from util.logger import setup_logging
from model.user import create_user, hash_pwd
from setting import default_setting, program_args
from app_define import USER_ROLE_MANAGER, USER_ROLE_USER, USER_ROLE_DATA, USER_ROLE_FIRST


if __name__ == '__main__':
    setup_mongodb_client()
    setup_logging()
    username = 'testuser3'
    pwd = '123456'
    name = '无权限'
    if not program_args.debug:
        pwd = hash_pwd(pwd, username)
    print(username, pwd)
    ret = create_user(username, pwd, USER_ROLE_FIRST, name)
    print(ret)
