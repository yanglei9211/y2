from elasticsearch_dsl import Keyword, Text, Integer, Nested

from model.es.base_model import EsBaseModel


class EsPacket(EsBaseModel):
    ALIAS = "packet_engine"
    ID = 'suit_packet_id'
    suit_packet_id = Keyword()
    username = Keyword()
    # name = Text(analyzer='ik_max_word', search_analyzer='ik_max_word')
    name = Text()
    edu = Integer()
    suit_papers = Nested()
    user_info = Nested()
    class Index:
        name = "packet_engine"

