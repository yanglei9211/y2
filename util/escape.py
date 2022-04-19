import json
from datetime import datetime, date

from bson import ObjectId
from bson.errors import InvalidId
from typing import Any, List, Optional, Dict
from fastapi.responses import Response, JSONResponse

from util.errors import DTError


def str_may_to_objectid(value):
    # return ObjectId(value)
    try:
        return True, ObjectId(value)
    except InvalidId:
        return False, value


def safe_objectid_from_str(value):
    # return ObjectId(value)
    try:
        return ObjectId(value)
    except InvalidId:
        raise DTError(u'数据%s 异常,非法ID' % value)


class SafeJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        if not content:
            content = {}
        if 'err_msg' not in content:
            content['err_msg'] = 'successful'
        if content['err_msg'] == 'successful':
            content['code'] = 0
        else:
            content['code'] = -1
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def safe_json_decode(value):
    try:
        return json.loads(value)
    except ValueError:
        raise Exception(400, 'bad string for json')


def json_encode(value, ensure_ascii=False, indent=None):
    def objectid_encoder(obj):
        type_encoders = [
            (ObjectId, str),
        ]
        for encoder in type_encoders:
            if isinstance(obj, encoder[0]):
                return encoder[1](obj)
        raise TypeError("Unknown value '%s' of type %s" % (
            obj, type(obj)))
    # adapted from tornado.escape.json_encode
    return json.dumps(
        value, default=objectid_encoder,
        ensure_ascii=ensure_ascii,
        indent=indent).replace("</", "<\\/")


def safe_typed_from_str(value, type_):
    try:
        return type_(value)
    except Exception as e:
        # raise HTTPError(400, "'%s' is not a '%s'" %
        #                 (value, value.__class__.__name__))
        raise DTError(u'数据{} -> {} 异常'.format(value, type_.__name__))

