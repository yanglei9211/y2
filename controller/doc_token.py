from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from controller.user import set_token_by_user
from util.escape import SafeJSONResponse
from util.logger import logger_time_cost

token_router = APIRouter()


# swagger登录用的
@token_router.post('/token')
@logger_time_cost
def login(form_data:  OAuth2PasswordRequestForm = Depends()):
    token = set_token_by_user(form_data)
    return SafeJSONResponse({'access_token': token, 'token_type': 'bearer'})
