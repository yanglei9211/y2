from datetime import timedelta, datetime

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.requests import Request
from jose import JWTError, jwt
from jose.constants import ALGORITHMS

from model.db_model.user import UserDbModel
from util.escape import SafeJSONResponse
from util.logger import logger_time_cost
from model.user import load_user_with_pwd
from setting import default_setting
from util.auth import UserAuthValidate


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_router = APIRouter()
pre_fix = '/api/y2/user/'


@user_router.post('/login')
@logger_time_cost
def login(form_data:  OAuth2PasswordRequestForm = Depends()):
    token = set_token_by_user(form_data)
    return SafeJSONResponse({'access_token': token, 'token_type': 'bearer'})


def set_token_by_user(form_data):
    um = load_user_with_pwd(form_data.username, form_data.password)
    expire = datetime.utcnow() + timedelta(seconds=int(default_setting.token_timeout))
    data = {
        'username': um.username,
        'exp': expire,
    }
    print(data)
    print(default_setting.secret_key)
    print(ALGORITHMS.HS256)
    token = jwt.encode(claims=data, key=default_setting.secret_key, algorithm=ALGORITHMS.HS256)
    return token


@user_router.get('/list')
@logger_time_cost
def user_list(request: Request, current_user: str = Depends(UserAuthValidate)):
    ret = UserDbModel.get_user_list()
    return SafeJSONResponse({'user_list': ret})
