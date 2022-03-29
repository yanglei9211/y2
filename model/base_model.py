from typing import Optional
from urllib.parse import urlencode

import httpx

from model.mongodb import get_client


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


class Item(BaseSubjectDbModel):
    TBL = 'items'


class BaseHttpModel(object):
    _model_name = ''
    _need_valid_req = True

    @classmethod
    def valid_req(cls, req):
        if req['code'] == 0 and not req['message']:
            return req
        else:
            msg = req.get('message', 'unknown')
            return {'msg': '内部调用错误:{}'.format(msg)}

    @classmethod
    async def asy_request(cls, method, host, url, data={}, headers=None, cookies=None):
        if headers and cookies:
            # TODO 有需要写headers的需要时再加
            pass
        url = host + url
        if method in ['get', 'Get', 'GET']:
            # 拼接参数
            query = urlencode(data)
            url = '{}?{}'.format(url, query)
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=30)

        elif method in ['post', 'Post', 'POST']:
            async with httpx.AsyncClient() as client:
                r = await client.post(url, data=data, timeout=30)
        else:
            # raise DTError('no method: {}'.format(method))
            return {'msg': 'no method: {}'.format(method)}
        if r.status_code != 200:
            raise Exception('内部调用错误,{}: {}'.format(
                cls._model_name, r.status_code))
        req = r.json()
        if (not cls._need_valid_req) or (cls._need_valid_req and cls.valid_req(req)):
            return req
        else:
            raise {'msg': '???'}

    @classmethod
    def request(cls, method, host, url, data={}, headers=None, cookies=None):
        if headers and cookies:
            # TODO 有需要写headers的需要时再加
            pass
        url = host + url
        if method in ['get', 'Get', 'GET']:
            query = urlencode(data)
            url = '{}?{}'.format(url, query)
            with httpx.Client() as client:
                r = client.get(url, timeout=30)
        elif method in ['post', 'Post', 'POST']:
            with httpx.Client() as client:
                r = client.post(url, data=data, timeout=30)
        else:
            return {'msg': 'no method: {}'.format(method)}
        if r.status_code != 200:
            raise Exception('内部调用错误,{}: {}'.format(
                cls._model_name, r.status_code))
        req = r.json()
        if (not cls._need_valid_req) or (cls._need_valid_req and cls.valid_req(req)):
            return req
        else:
            return {'msg': '???'}
