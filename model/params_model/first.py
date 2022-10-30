from pydantic import BaseModel, Field


class ItemInsertParamModel(BaseModel):
    sid: str = Field(..., description="sid")
    name: str = Field(..., description="name")

class RedisSetParamModel(BaseModel):
    key: str = Field(..., description="key")
    value: str = Field(..., description="value")
    exp: int = Field(..., description="value")
