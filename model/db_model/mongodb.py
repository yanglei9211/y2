from pymongo import MongoClient

from util.logger import Logging
from setting import mongodb_setting as m_setting


class MongoDbClient(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            Logging.info('connecting mongodb: {}'.format(m_setting.mongodb_url))
            cls.instance = super(MongoDbClient, cls).__new__(cls)
            cls.client = MongoClient(host=m_setting.mongodb_url, replicaSet=m_setting.replica_set,
                                     w=m_setting.w_value, wtimeout=m_setting.wtimeout)
            Logging.info('connect mongodb success')
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
    return MongoDbClient().get_client()


def setup_mongodb_client():
    MongoDbClient()
