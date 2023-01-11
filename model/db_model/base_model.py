from typing import Optional
from urllib.parse import urlencode

import httpx

from model.db_model.mongodb import get_client


klx_db_map = {
    'chinese': 'klx_xchi',
    'math': 'klx_xmath',
    'english': 'klx_xen',
    'physics': 'klx_xph',
    'chemistry': 'klx_xch',
    'biology': 'klx_xbi',
    'history': 'klx_xhi',
    'geography': 'klx_xge',
    'politics': 'klx_xpo',
    'history_society': 'klx_xso',
    'information': 'klx_xin',
    'generic_technology': 'klx_xgt',
    'science': 'klx_xsc',
    'zonghe': 'klx_zonghe',
    'french': 'klx_xfr',
    'japanese': 'klx_xja',
    'russian': 'klx_xru',
    'other1': 'klx_xot1',
    'other2': 'klx_xot2',
    'art': 'klx_xart',
    'music': 'klx_xmu',
    'physical_education': 'klx_Itemxpe',
    'case_analysis': 'klx_xcase',
}


class BaseDbModel:
    @classmethod
    def find_by_id(cls, _id) -> Optional[dict]:
        col = get_client()[cls.DB][cls.TBL]
        res = col.find_one({'_id': _id})
        return res


class BaseSubjectDbModel:
    @classmethod
    def find_by_id(cls, subject, _id) -> Optional[dict]:
        DB = klx_db_map[subject]
        print(4, id(get_client()))
        col = get_client()[DB][cls.TBL]
        res = col.find_one({'_id': _id})
        return res

    @classmethod
    def find_by_ids(cls, subject, ids, projection=[]) -> list:
        DB = klx_db_map[subject]
        col = get_client()[DB][cls.TBL]
        if projection and isinstance(projection, list):
            res = list(col.find({'_id': {'$in': ids}}, projection=projection))
        else:
            res = list(col.find({'_id': {'$in': ids}}))
        return res


class Item(BaseSubjectDbModel):
    TBL = 'items'

class KnowledgeTags(BaseSubjectDbModel):
    TBL = 'knowledge_tags'

class SuitPacket(BaseSubjectDbModel):
    TBL = 'suit_packet'