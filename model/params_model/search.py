from typing import List

from pydantic import BaseModel, Field

class SearchItemUpsertParamModel(BaseModel):
    subject: str = Field(..., description="学科")
    item_id: str = Field(..., description="item_id")

class SearchItemSearchParamModel(BaseModel):
    subject: str = Field(..., description="学科")
    keyword: str = Field(..., description="关键字")


class BaseItemInfoModel(BaseModel):
    item_id: str = Field(..., description='item_id')
    text: str = Field(..., description='文本信息')

class SearchItemSearchRespModel(BaseModel):
    items: List[BaseItemInfoModel] = Field(..., description='题目')

