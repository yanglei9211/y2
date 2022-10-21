import json

from util.logger import Logging
from setting import redis_setting as r_setting
from redis import StrictRedis

default_exptime = 86400

class RedisClient(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            Logging.info('connecting redis: {}'.format(r_setting.redis_url))
            cls.instance = super(RedisClient, cls).__new__(cls)
            rclient = StrictRedis.from_url(r_setting.redis_url, db=r_setting.redis_db,
                                           socket_timeout=r_setting.redis_timeout)
            rclient.exists("dumb_key_test_connectivity")  # force to connect
            cls.client = rclient
            Logging.info("Redis connected. Seems good.")
            Logging.info('connect redis success')
        return cls.instance

    @classmethod
    def get_client(cls):
        return cls.client

    @classmethod
    def close(cls):
        c = cls.get_client()
        c.close()

def get_client() -> StrictRedis:
    return RedisClient().get_client()

def setup_redis_client():
    RedisClient()

def set_cache(key, value, exp=None):
    c = get_client()
    c.set(key, value, ex=exp)
    Logging.info("push into redis, key :{}, value:{}".format(key, value))

def get_cache(key):
    c = get_client()
    ret = c.get(key)

    if ret:
        Logging.info("found key:{} value:{}".format(key, ret))
        return True, ret
    else:
        Logging.info("key:{} not found".format(key))
        return False, ""


def set_hash_cache(name, mapping):
    c = get_client()
    ret = c.hset(name, mapping=mapping)
    return ret


def get_hash_cache(name, key):
    c = get_client()
    ret = c.hget(name, key)
    return ret

def get_hash_mcache(name, keys):
    c = get_client()
    ret = c.hmget(name, keys)
    return ret


def del_hash_cache(name, keys):
    c = get_client()
    ret = c.hdel(name, *keys)
    return ret


def set_knowledge_tree(subject, tree):
    set_hash_cache('item_engine3_ktree_{}'.format(subject), tree)


def del_knowledge_tree(subject):
    c = get_client()
    c.delete('item_engine3_ktree_{}'.format(subject))


def get_knowledge_tree(subject, keys):
    keys = [str(key) for key in keys]
    values = get_hash_mcache('item_engine3_ktree_{}'.format(subject), keys) if keys else []
    values = [json.loads(value) for value in values]
    return values
