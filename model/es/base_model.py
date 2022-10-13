from datetime import datetime

from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import connections, Document
from elasticsearch_dsl.connections import create_connection
from fnmatch import fnmatch

from util.logger import Logging
from setting import es_setting

class EsBaseModel(Document):

    @classmethod
    def _matches(cls, hit):
        return fnmatch(hit["_index"], '*_{}-*'.format(cls.ALIAS))

    @classmethod
    def alias(cls,subject):
        return '{}_{}'.format(subject, cls.ALIAS)

    @classmethod
    def find(cls):
        pass

    @classmethod
    def create_index(cls, subject):
        es = get_dsl_client()
        index_template = cls._index.as_template(cls.ALIAS, '*_{}-*'.format(cls.ALIAS))
        print(index_template.to_dict())
        print("-=-"*12)
        index_template.save(using=es)
        next_index = '{}_{}-{}'.format(subject, cls.ALIAS, datetime.now().strftime("%Y%m%d%H%M%S%f"))
        es.indices.create(index=next_index)
        return next_index

    @classmethod
    def realias(cls, subject, next_index):
        alias = '{}_{}'.format(subject, cls.ALIAS)
        pattern = '{}_{}-*'.format(subject, cls.ALIAS)
        es = get_dsl_client()
        es.indices.update_aliases(
            body={
                'actions': [
                    {'remove': {'alias': alias, 'index': pattern}},
                    {'add': {'alias': alias, 'index': next_index}}
                ]
            }
        )
        return alias

    @classmethod
    def update_one(cls, subject, **data):
        index_name = '{}_{}'.format(subject, cls.ALIAS)
        Logging.info('update, index_name={}'.format(index_name))
        cls._get_connection().update(
            index=index_name,
            id=data[cls.ID],
            doc_type='doc',
            body={
                'doc': data,
                'doc_as_upsert': True
            }
        )

    @classmethod
    def update_many(cls, subject, datas, index_name=None, refresh=True):
        index_name = index_name if index_name else '{}_{}'.format(subject, cls.ALIAS)
        Logging.info('update many, index_name={}'.format(index_name))
        actions = []
        es = get_es_client()
        ids = []
        for data in datas:
            ids.append(data[cls.ID])
            actions.append({
                '_op_type': 'index',
                '_index': index_name,
                '_type': 'doc',
                '_id': data[cls.ID],
                '_source': data,
            })
        helpers.bulk(es, actions, refresh=refresh)




class EsClient(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EsClient, cls).__new__(cls)
            hosts = es_setting.es_host.split(',')
            cls.client = Elasticsearch(hosts)
            cls.dsl_client = create_connection(alias="default", hosts=hosts)
        return cls.instance

    @classmethod
    def get_client(cls):
        return cls.client

    @classmethod
    def get_dsl_client(cls):
        return cls.dsl_client

def get_es_client() -> Elasticsearch:
    return EsClient().get_client()

def get_dsl_client() -> connections.create_connection:
    return EsClient().get_dsl_client()

def setup_es_client():
    EsClient()

class BaseSearchEngine(object):
    pass