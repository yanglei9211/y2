from elasticsearch_dsl import Search, Q

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
        page_size = self.criteria.get('page_size', 20)
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
        # set_mode = self.criteria.get('set_mode', 'union')
        # node_mode = self.criteria.get('node_mode', 'group')
        self.filter_q.append(Q('terms', tag_ids=value))


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
