from pprint import pprint

from elasticsearch_dsl import Search, Q

from model.db_model.redis import get_knowledge_tree
from model.es.base_model import get_dsl_client
from util.logger import Logging

class SearchEngine(object):
    FILTER_KEYS = ['item_type', 'item_subtype']
    MUST_KEYS = []
    MUST_NOT_KEYS = []

    def __init__(self, subject, es_index, **kwargs):
        self.s = Search(using=get_dsl_client(), index=es_index.alias(subject))
        self.subject = subject
        self.filter_q = []
        self.must_q = []
        self.must_nq = []
        self.criteria = kwargs
        self.sort_params = None

    def search(self):
        Logging.info('filter_q: {}'.format(self.filter_q))
        Logging.info('must_q: {}'.format(self.must_q))
        Logging.info('must_nq: {}'.format(self.must_nq))
        query = Q('bool', filter=self.filter_q, must=self.must_q, must_not=self.must_nq)
        s = self.s.query(query)
        page_idx = self.criteria.get('page_idx', 0)
        page_size = self.criteria.get('page_size', 100)
        print("sort params")
        pprint(self.sort_params)
        if self.sort_params:
            s = s.sort(self.sort_params)
        s = s[page_idx*page_size: page_idx*page_size+page_size]  # 语法糖
        res = s.execute()
        s_log = s.to_dict()
        Logging.info(s_log.get('query', {}))
        return res.hits

    def count(self):
        Logging.info('filter_q: {}'.format(self.filter_q))
        Logging.info('must_q: {}'.format(self.must_q))
        Logging.info('must_nq: {}'.format(self.must_nq))
        query = Q('bool', filter=self.filter_q, must=self.must_q, must_not=self.must_nq)
        s = self.s.query(query)
        res = s.count()
        s_log = s.to_dict()
        Logging.info(s_log.get('query', {}))
        return res

    def filling(self):
        for key, value in self.criteria.items():
            if value and not isinstance(value, list):
                value = [value]
            if key in self.FILTER_KEYS:
                self.filter_q.append(Q('terms', **{key: value}))
            elif key in self.MUST_KEYS:
                self.must_q.append(Q('terms', **{key: value}))
            elif key in self.MUST_NOT_KEYS:
                self.must_nq.append(Q('terms', **{key: value}))
            else:
                self.filling_extra(key, value)

    def filling_tags(self, value):
        # 默认并集取题
        # set_mode = self.criteria.get('set_mode', 'union')
        # node_mode = self.criteria.get('node_mode', 'group')
        # self.filter_q.append(Q('terms', tag_ids=value))

        tags = get_knowledge_tree(self.subject, value)
        main_tag_ids = []
        used_tag_ids = []
        for tag in tags:
            used_tag_ids += tag['group']
        self.filter_q.append(Q('terms', tag_ids=used_tag_ids))


    def filling_extra(self, key, value):
        if key == 'tag_ids':
            self.filling_tags(value)
        elif key == 'keyword':
            value = ' '.join(value)
            keywords = [keyword for keyword in value.split() if keyword]
            for keyword in keywords:
                sub_q = [Q('match_phrase', stem={'query': keyword, 'slop': 1, 'boost': 1}),
                         Q('match_phrase', questions={'query': keyword, 'slop': 1, 'boost': 1}),
                         Q('match_phrase', answers={'query': keyword, 'slop': 1, 'boost': 0.01})
                         ]
                self.must_q.append(Q('bool', should=sub_q))


    def filling_sort(self):
        if self.criteria.get('sort_params', None):
            pprint(self.criteria['sort_params'])
            self.sort_params = {
                "_script": {
                    "script": {"id": "engine_sort_default",
                               "params": {"sort_params": self.criteria.get("sort_params")}},
                    "order": "desc",
                    "type": "number"
                }
            }


def generate_define_sort(subject, **kwargs):
    sort_params = []
    if kwargs.get('tag_ids'):
        tag_point_map = generate_tag_ids_sort_points(subject, kwargs['tag_ids'])
    else:
        tag_point_map = {}
    sort_params.append({
        'key': 'tag_ids',
        'type': 'list',
        'params': tag_point_map,
        'weight': 1
    })
    return sort_params


def generate_tag_ids_sort_points(subject, tag_ids):
    tag_point_map = {}
    current_point = 10
    while tag_ids and current_point > 0.1**10:
        # 设置最小值防止万一出现的无限循环
        tags = get_knowledge_tree(subject, tag_ids)
        next_tag_ids = []
        for tag in tags:
            if tag.get('tree_type') == 'knowledge_tag':
                tag_id = tag['_id']
                tag_point_map[tag_id] = max(tag_point_map.get(tag_id, 0), current_point)
                next_tag_ids += tag.get('children', [])
            elif tag.get('tree_type') == 'knowledge_point':
                for tag_id in tag.get('tag_ids'):
                    tag_point_map[tag_id] = max(tag_point_map.get(tag_id, 0), current_point)
                next_tag_ids += tag.get('children', []) + tag.get('tag_ids')
        current_point *= 0.1
        tag_ids = next_tag_ids
    return tag_point_map

