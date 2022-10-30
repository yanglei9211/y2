from bson import ObjectId
from fastapi import APIRouter, Depends, UploadFile, File, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from starlette.requests import Request

from model.db_model.redis import get_cache, set_cache
from model.params_model.first import ItemInsertParamModel, RedisSetParamModel
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


@first_router.post("/files", tags=['测试'])
async def create_file(filename: str, file: bytes = File(...)):
    ret = {
        'filename': filename,
        'size': len(file)
    }
    return SafeJSONResponse(ret)


@first_router.get("/item/get", tags=['测试'])
def get_item_by_sid(sid: str=Query(..., description="sid")):
    Logging.info("sid: {}".format(sid))
    ret = Item.find_by_sid(sid)
    return SafeJSONResponse(ret)

@first_router.get("/item/count", tags=['测试'])
def count_item():
    cnt = Item.count_docs()
    ret = {'total': cnt}
    return SafeJSONResponse(ret)

@first_router.post("/item/insert", tags=['测试'])
def insert_item(args: ItemInsertParamModel):
    Logging.info("insert item sid:{}, name:{}".format(args.sid, args.name))
    Item.insert_doc(args.sid, args.name)
    return SafeJSONResponse()

@first_router.get("/redis/get", tags=['测试'])
def redis_get(key: str=Query(..., description=("key"))):
    v = get_cache(key)
    ret = {'value': v}
    return SafeJSONResponse(ret)


@first_router.post("/redis/set", tags=['测试'])
def redis_set(args: RedisSetParamModel):
    set_cache(args.key, args.value, args.exp)
    return SafeJSONResponse()
