from elasticsearch_dsl import Keyword, Integer, Text, Boolean, Long, Nested

from model.db_model.base_model import Item
from model.es.base_model import EsBaseModel


class EsItem(EsBaseModel):
    ALIAS = "item_engine"
    ID = 'item_id'
    item_id = Keyword()
    sources = Keyword()
    tag_ids = Keyword()
    item_type = Keyword()
    item_subtype = Keyword()
    # stem = Text(analyzer='ik_max_word', search_analyzer='ik_max_word')
    # questions = Text(analyzer='ik_max_word', search_analyzer='ik_max_word')
    # answers = Text(analyzer='ik_max_word', search_analyzer='ik_max_word')
    stem = Text()
    questions = Text()
    answers = Text()
    class Index:
        name = "item_engine"




