from pprint import pprint
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel, Field

from starlette.requests import Request

from util.errors import DTError
from util.escape import SafeJSONResponse
from util.logger import async_logger_time_cost

search_route = APIRouter()

class SearchTestParamModel(BaseModel):
    item_ids: List[int] = Field(..., description="item_ids")
    

class DocTest(BaseModel):
    item_id: int
    paper_ids: List[int]
    
    # def __init__(self, item_id, paper_ids):
    #     self.item_id = item_id
    #     self.paper_ids = paper_ids
    #     super(DocTest, self).__init__()
    
    
class SearchTestRespModel(BaseModel):
    docs: List[DocTest] = Field(..., description="tdocs")
    

@search_route.post("/tdoc", response_model=SearchTestRespModel)
@async_logger_time_cost
async def search_test(args: SearchTestParamModel):
    tdoc = DocTest(item_id=1, paper_ids=[1,2])
    resp = SearchTestRespModel(docs=[tdoc])
    return SafeJSONResponse(resp)


    



