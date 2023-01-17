from pprint import pprint
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Query
from pydantic import BaseModel, Field
from elasticsearch_dsl import Q,A,Search
from starlette.requests import Request

from bl.search import item2es_item, search_items
from model.db_model.base_model import Item
from model.db_model.redis import set_cache, get_cache, get_knowledge_tree
from model.es.item import EsItem
from model.es.suit_packet import EsPacket
from model.params_model.search import SearchItemUpsertParamModel, SearchItemSearchRespModel, SearchItemSearchParamModel, \
    BaseItemInfoModel, SearchRedisSetParamModel, SearchRedisGetRespModel, SearchPacketSearchParamModel
from util.errors import DTError
from util.escape import SafeJSONResponse, safe_objectid_from_str
from util.logger import async_logger_time_cost, logger_time_cost, Logging
from model.es.base_model import get_dsl_client, get_es_client

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
    s = Search(using=get_dsl_client(), index="tyc_indexs")
    s = s.filter('terms', **{'paper_id': [1]})
    for hit in s:
        print(hit)
    resp = SearchTestRespModel(docs=[tdoc])
    return SafeJSONResponse(resp)


@search_route.post("/tengine/item/upsert")
@logger_time_cost
def upsert_item(args: SearchItemUpsertParamModel):
    item_id = safe_objectid_from_str(args.item_id)
    subject = args.subject
    it = Item.find_by_id(subject, item_id)
    es_item = item2es_item(it)
    # EsItem.update_one(subject, **es_item)
    EsItem.update_many(subject, [es_item])
    return SafeJSONResponse()

@search_route.post("/tengine/item/search", response_model=SearchItemSearchRespModel)
@logger_time_cost
def search_item(args: SearchItemSearchParamModel):
    print(args.subject)
    print(args.keyword)
    print(args.tag_ids)
    total, items = search_items(args)
    # print(total, item_ids)
    resp = SearchItemSearchRespModel(total=total, items=[])
    for i in items:
        resp.items.append(BaseItemInfoModel(item_id=i['item_id'], text=i['item_text']))

    return SafeJSONResponse(resp)


@search_route.post("/tengine/packet/search")
@logger_time_cost
def search_packet(args: SearchPacketSearchParamModel):
    Logging.info(args.subject, args.cnt)
    client = get_es_client()
    s = Search(using=client, index=EsPacket.alias('math'))
    # s = s.query("match", suit_packet_id='5f6c18ba84da5a37fc6919d8')
    # s = Search().using(client).query("match", suit_packet_id='5f6c18ba84da5a37fc6919d8')
    # s = s.filter('terms', edu=[2,3,4])
    # print(s.count())
    # s = s.query("range", use_info__term__use={'gt': 0})
    # s = s.filter("terms", edu=[2,3,4])
    # s = s.sort('use_info.term.use')
    # s.script_fields()
    # s = s.script_fields(sort_num={
    #     'script': {
    #         'lang':"painless",
    #         'source': "doc['use_info.term.use'].value*2"
    # }})
    # s = s.sort(
    #     {"_script": {
    #                 "script": {
    #                     'lang': "painless",
    #                     'source': "doc['use_info.term.use'].value*2"
    #                 },
    #                 "order": "asc",
    #                 "type": "number"
    #             }}
    # )
    tp = 'sum'
    a = A(tp, field='edu')
    # a = A()
    s.aggs.bucket(tp, a)
    s = s[0:15]
    s = s.execute()
    print(len(s))
    pprint(s.aggs.to_dict())
    for hit in s:
        # pprint(hit)
        d = hit.to_dict()
        print(d['name'], d['suit_packet_id'], d['edu'])
        # pprint(d)
    return SafeJSONResponse()




@search_route.post("/tengine/redis/set")
@logger_time_cost
def redis_set_kv(args: SearchRedisSetParamModel):
    set_cache(args.k, args.v, args.exp)
    return SafeJSONResponse()


@search_route.get("/tengine/redis/get", response_model=SearchRedisGetRespModel)
@logger_time_cost
def redis_get_k(k: str = Query(..., description="k")):
    found, ret = get_cache(k)
    resp = SearchRedisGetRespModel(hit=found, v=ret)
    return SafeJSONResponse(resp)


@search_route.get("/tengine/tag_tree")
@logger_time_cost
def watch_tag_tree(subject: str = Query(..., description='学科'),
                   tag_ids: List[str] = Query(..., description='知识点id')):
    tag_ids = list(map(safe_objectid_from_str, tag_ids))
    ret = get_knowledge_tree(subject, tag_ids)
    pprint(ret)
    return SafeJSONResponse()