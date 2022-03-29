from typing import Optional

from bson import ObjectId
from fastapi import APIRouter
from starlette.requests import Request

from util.escape import SafeJSONResponse
from util.logger import Logging, logger_time_cost
from util.errors import DTError
from model.base_model import Item

first_router = APIRouter()


@first_router.get("/", tags=['测试'])
@logger_time_cost
def read_root(request: Request):
    Logging.error("Welcome get from: {}".format(request.client.host))
    return {"Welcome": "Resource_config"}


@first_router.get("/items", tags=['测试'])
@logger_time_cost
def load_item(item_id: str, request: Request):
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