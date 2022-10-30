from typing import Optional

from pymongo import MongoClient

from util.logger import Logging
from setting import mongodb_setting as m_setting

_client: Optional[MongoClient] = None

class MongoDbClient(object):

    @classmethod
    def connect_mongodb(cls, host, wtimeout):
        client = MongoClient(host=host, wtimeout=wtimeout)
        return client

    @classmethod
    def connect_mongodb_replica_set(cls, host, replicaSet, w, wtimeout):
        client = MongoClient(host=host, replicaSet=replicaSet, w=w, wtimeout=wtimeout)
        return client
    def __new__(cls):
        Logging.info("*************check instance before: {}".format(hasattr(cls, 'instance')))
        if not hasattr(cls, 'instance'):
            cls.instance = super(MongoDbClient, cls).__new__(cls)
            if m_setting.replica_set != "":
                Logging.info('connecting mongodb replica_set: {}'.format(m_setting.mongodb_url))
                cls.client = MongoClient(host=m_setting.mongodb_url, replicaSet=m_setting.replica_set,
                                         w=m_setting.w_value, wtimeout=m_setting.wtimeout)
            else:
                Logging.info('connecting mongodb: {}'.format(m_setting.mongodb_url))
                cls.client = cls.connect_mongodb(m_setting.mongodb_url, m_setting.wtimeout)
            Logging.info('connect mongodb success')
        Logging.info("*************check instance after: {}".format(hasattr(cls, 'instance')))
        return cls.instance

    @classmethod
    def get_client(cls):
        # logger.info('id mongo client: {}'.format(id(cls.client)))
        return cls.client

    @classmethod
    def close(cls):
        c = cls.get_client()
        c.close()


def get_client() -> MongoClient:
    # global _client
    # return _client
    return MongoDbClient().get_client()


def setup_mongodb_client():
    MongoDbClient()
    # global _client
    # _client = MongoDbClient().get_client()



