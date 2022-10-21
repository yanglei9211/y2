from typing import List

from pydantic import BaseModel, Field

class SearchItemUpsertParamModel(BaseModel):
    subject: str = Field(..., description="学科")
    item_id: str = Field(..., description="item_id")

class SearchItemSearchParamModel(BaseModel):
    subject: str = Field(..., description="学科")
    keyword: str = Field(..., description="关键字")
    tag_ids: List[str] = Field(..., description="知识点")


class BaseItemInfoModel(BaseModel):
    item_id: str = Field(..., description='item_id')
    text: str = Field(..., description='文本信息')

class SearchItemSearchRespModel(BaseModel):
    total: int = Field(..., description="题量")
    items: List[BaseItemInfoModel] = Field(..., description='题目')


class SearchRedisSetParamModel(BaseModel):
    k: str = Field(..., description='key')
    v: str = Field(..., description='value')
    exp: int = Field(..., description='exp')

class SearchRedisGetParamModel(BaseModel):
    k: str = Field(..., description='key')

class SearchRedisGetRespModel(BaseModel):
    v: str = Field(..., description='v')
    hit: bool= Field(..., description='hit')

