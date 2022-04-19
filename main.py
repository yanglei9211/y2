import traceback
from typing import Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from controller.doc_token import token_router
from controller.first import first_router
from controller.user import user_router
from model.db_model.mongodb import setup_mongodb_client
from setting import program_args
from util.escape import SafeJSONResponse
from util.errors import DTError
from util.logger import setup_logging, Logging

fake_user = {'admin': {
    'username': 'admin',
    'password': '123456',
    'phone': '12345678',
    'name': 'test'
}}


class UserModel(BaseModel):
    username: str
    password: str
    phone: Optional[str] = None
    name: str


def hash_password(s):
    return s


app = FastAPI()
app.include_router(first_router, prefix='/api/y2/test', tags=['测试'])
app.include_router(user_router, prefix='/api/y2/user', tags=['账号'])
app.include_router(token_router, tags=['swagger'])


@app.exception_handler(DTError)
async def data_error_handler(request, exc):
    return SafeJSONResponse({'err_msg': exc})


@app.exception_handler(Exception)
async def system_exception_handler(request, exc):
    emsg = traceback.format_exc()
    exc = str(exc) + "\n" + emsg
    Logging.error(exc)
    return SafeJSONResponse({'err_msg': exc})


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def fake_decode_token(token):
#     user = fake_user.get(token)
#     return user
#
#
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise Exception('user: {} not found'.format(user))
#     return user
#
#
# def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
#     return current_user
#
#
# @app.get('/user/me', tags=['登录'])
# def read_item(current: UserModel = Depends(get_current_user)):
#     return current
#
#
# @app.get('/token', tags=['登录'])
# def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}
#
#
# @app.post('/token', tags=['登录'])
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_user.get(form_data.username)
#     if not user_dict:
#         raise Exception('user:{} not found'.format(form_data.username))
#     user = UserModel(**user_dict)
#     hashed_pwd = hash_password(form_data.password)
#     if not hashed_pwd == user.password:
#         raise Exception('pwd error')
#     return {'access_token': user.username, 'token_type': 'bearer'}


def start_server():
    host = '0.0.0.0'
    port = program_args.port
    setup_mongodb_client()
    setup_logging()
    # init_logger()

    uvicorn.run(app="main:app", host=host, port=port, reload=True, debug=True)


def close_server():
    pass


if __name__ == "__main__":
    start_server()
