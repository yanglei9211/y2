from typing import Optional
from urllib.parse import urlencode

import httpx

from model.db_model.mongodb import get_client


class BaseDbModel:
    DB=''
    TBL=''
    @classmethod
    def find_by_id(cls, _id) -> Optional[dict]:
        col = get_client()[cls.DB][cls.TBL]
        res = col.find_one({'_id': _id})
        return res




class Item(BaseDbModel):
    DB = "dbtest"
    TBL = "item"
    @classmethod
    def find_by_sid(cls, _sid):
        col = get_client()[cls.DB][cls.TBL]
        res = col.find_one({'sid': _sid})
        return res


    @classmethod
    def count_docs(cls):
        col = get_client()[cls.DB][cls.TBL]
        ret = col.count()
        return ret

    @classmethod
    def insert_doc(cls, sid, name):
        col = get_client()[cls.DB][cls.TBL]
        col.insert({'sid': sid, 'name': name})
        return

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
