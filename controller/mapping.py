from fastapi import APIRouter, Query

from app_define import CODE_2_SUBJECT
from model.mapping import MappingTextbook, MappingTextbookVer, MappingRawType, MappingTag
from util.errors import DTError
from util.escape import str_may_to_objectid, SafeJSONResponse, safe_typed_from_str
from pydantic import BaseModel, Field
from starlette.requests import Request

from util.logger import Logging

reflect_router = APIRouter()


@reflect_router.get("/resource/mapping", description="获取映射", tags=['映射'])
def get_resource_mapping(resource_type: str =
                         Query(..., description="资源类型: ['tag', 'textbook', 'textbook_ver','raw_type', "
                                                "'business_type']"),
                         resource_id: str = Query(..., description="资源id"),
                         resource_from: str = Query(..., description="来源: [oto, klx, sq]"),
                         resource_to: str = Query(..., description="去向: [oto, klx, sq]")):
    if resource_type not in ['tag', 'textbook', 'textbook_ver', 'raw_type', 'business_type']:
        return SafeJSONResponse({'err_msg': 'resource_type: {} 非法'.format(resource_type)})
    _, resource_id = str_may_to_objectid(resource_id)
    # target_id = 'simple_resource_id'
    if resource_type == 'textbook':
        target = MappingTextbook.get_mapping(resource_id, resource_from, resource_to)
        target_id = target['target_id']
    elif resource_type == 'textbook_ver':
        target = MappingTextbookVer.get_mapping(resource_id, resource_from, resource_to)
        target_id = target['target_id']
    elif resource_type == 'raw_type':
        resource_id = safe_typed_from_str(resource_id, int)
        target = MappingRawType.get_mapping(resource_id, resource_from, resource_to)
        target_id = target['target_id']
    elif resource_type == 'tag':
        _, resource_id = str_may_to_objectid(resource_id)
        target = MappingTag.get_mapping(resource_id, resource_from, resource_to)
        target_id = target['target_id']
    else:
        raise DTError('resource_type: {} 非法'.format(resource_type))
    return SafeJSONResponse({'target_id': target_id})


@reflect_router.get("/rich_resource/mapping", description="获取映射", tags=['映射'])
def get_rich_resource_mapping(resource_type: str =
                              Query(..., description="资源类型: [suit_paper, item]"),
                              subject: str = Query(..., description="学科"),
                              edu: int = Query(..., description="学段: [2,3,4]"),
                              resource_id: str = Query(..., description="资源id"),
                              resource_from: str = Query(..., description="来源: [oto, klx, sq]"),
                              resource_to: str = Query(..., description="去向: [oto, klx, sq]")):
    subject_code = CODE_2_SUBJECT[subject][edu]
    if resource_from == 'klx' and resource_to == 'sq':
        if resource_type == 'item':
            return SafeJSONResponse({'target_id': 'Q_{}_{}'.format(subject_code, str(resource_id))})
        elif resource_type == 'suit_paepr':
            return SafeJSONResponse({'target_id': 'P_{}_{}'.format(subject_code, str(resource_id))})
        else:
            return SafeJSONResponse({'err_msg': 'resource_type: {} 非法'.format(resource_type)})
    else:
        return SafeJSONResponse({'err_msg': 405})


@reflect_router.get("/subject/mapping", description="获取映射", tags=['映射'])
def get_subject_mapping(subject: str = Query(..., description="学科"),
                        edu: int = Query(..., description="学段: [2,3,4]"),):
    subject_code = CODE_2_SUBJECT[subject][edu]
    return SafeJSONResponse({'subject_id': subject_code})


class ReflectAddArgsModel(BaseModel):
    resource_type: str = Field(..., description='资源类型,[tag, textbook, suit_paper, item, item_type]')
    resource_id: str = Field(..., description='资源id')
    target_id: str = Field(..., description='转化后资源id')
    resource_from: str = Field(..., description="来源: [oto, klx, sq]")
    resource_to: str = Field(..., description="去向: [oto, klx, sq]")


@reflect_router.post("/resource/add", description="新增映射", tags=['映射'])
def add_resource_reflect(arg: ReflectAddArgsModel, request: Request):
    Logging.info('\nadd reflect \n resource_type: {}, resource_id: {}, target_id: {}, resource_from: {}'
                 'resource_to: {}'.format(arg.resource_type, arg.resource_id, arg.target_id,
                                         arg.resource_from, arg.resource_to
    ))
    return SafeJSONResponse()
