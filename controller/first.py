from bson import ObjectId
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from starlette.requests import Request

from util.auth import DataAuthValidate
from util.escape import SafeJSONResponse, safe_objectid_from_str
from util.logger import Logging, logger_time_cost
from model.db_model.base_model import Item
from model.user import get_current_user

first_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# 登录校验


@first_router.get("/", tags=['测试'])
@logger_time_cost
def read_root(request: Request):
    Logging.error("Welcome get from: {}".format(request.client.host))
    return {"Welcome": "y2"}


@first_router.get("/items", tags=['测试'])
@logger_time_cost
def load_item(item_id: str,  request: Request, token: str = Depends(oauth2_scheme)):
    ret = Item.find_by_id('math', ObjectId(item_id))
    return SafeJSONResponse({'item': ret})


# @first_router.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
#
#
# @first_router.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}

class LoadItemModel(BaseModel):
    item_id: str = Field(..., description='题目id')
    subject: str = Field(..., description='学科')


@first_router.post("/items", tags=['测试'])
@logger_time_cost
def post_load_item(args: LoadItemModel, request: Request, token: str = Depends(DataAuthValidate)):
    print(str)
    ret = Item.find_by_id(args.subject, safe_objectid_from_str(args.item_id))
    return SafeJSONResponse({'item': ret})
