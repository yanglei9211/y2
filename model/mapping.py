from model.base_model import BaseDbModel
from model.mongodb import get_client


class BaseMapping(BaseDbModel):
    _DB = 'klx_migrate'
    _COL_MAP = {
        'textbook': 'mapping_textbook',
        'textbook_ver': 'mapping_textbook_ver',
        'tag': 'mapping_tag',
        'item_type': 'mapping_item_type',
        'suit_paper': 'mapping_suit_paper',
        'item': 'mapping_item',
        'raw_type': 'mapping_raw_type'
    }

    @classmethod
    def get_mapping(cls, resource_id, f, t):
        cname = cls.get_cname()
        col = get_client()[cls._DB][cname]
        print(col)
        print({'resource_id': resource_id, 'from': f, 'to': t})
        ret = col.find_one({'resource_id': resource_id, 'from': f, 'to': t})
        return ret

    @classmethod
    def get_cname(cls):
        return None


class MappingTextbook(BaseMapping):
    @classmethod
    def get_cname(cls):
        return 'mapping_textbook'


class MappingTextbookVer(BaseMapping):
    @classmethod
    def get_cname(cls):
        return 'mapping_textbook_ver'


class MappingRawType(BaseMapping):
    @classmethod
    def get_cname(cls):
        return 'mapping_raw_type'


class MappingTag(BaseMapping):
    @classmethod
    def get_cname(cls):
        return 'mapping_tag'
