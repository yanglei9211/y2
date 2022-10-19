from pprint import pprint

from elasticsearch_dsl import Q, Search

from bl.search_engine import SearchEngine
from model.es.base_model import get_dsl_client
from model.es.item import EsItem


def item2es_item(it):
    tag_ids = it['data'].get('tag_ids', [])
    questions = []
    answers = []
    for q in it['data'].get('qs', []):
        tag_ids.extend(q.get('tag_ids', []))
        if q.get('desc'):
            questions.append(q['desc'])
        answers.append(q['ans'])
        for sq in q.get('qs', []):
            tag_ids.extend(sq.get('tag_ids', []))
            if sq.get('desc'):
                questions.append(sq['desc'])
            answers.append(sq['ans'])
    tag_ids = list(set(tag_ids))
    tag_ids = [str(x) for x in tag_ids]
    es_item = {
        'item_id': str(it['_id']),
        'sources': it['data']['classes'],
        'tag_ids': tag_ids,
        'item_type': it['data']['type'],
        'item_subtype': it['data']['subtype'],
        'stem': it['data']['stem'],
        'questions': questions,
        'answers': answers,
    }
    return es_item

def item2text(eit):

    i = eit['_source']
    cur = i['stem']
    cur += "\n".join(i['questions'])
    ass = [str(j) for j in i['answers']]
    cur += "\n".join(ass)
    return cur

def search_by_keyword_bak(subject, keyword):
    client = get_dsl_client()
    # sub_q = [Q('match_phrase', stem={'query': keyword, 'slop': 1, 'boost': 1}),
    #          Q('match_phrase', questions={'query': keyword, 'slop': 1, 'boost': 1}),
    #          Q('match_phrase', answers={'query': keyword, 'slop': 1, 'boost': 0.1})]
    sub_q = [Q('term', stem={'query': keyword}),
            Q('term', stem={'query': keyword})]

    query = Q('bool', should=sub_q)
    s = Search(using=client, index=EsItem.alias(subject))
    s = s.query(query)
    res = s.execute()
    res = res.hits
    item_ids = []
    total = res.total
    texts = item2text(res.hits)
    for hit in res.hits:
        item_id = hit['_id']
        item_ids.append(item_id)
        # pprint(hit)
    return texts, item_ids

def search_items(search_item_params):
    tag_ids = search_item_params.tag_ids
    params = {
        'keyword': search_item_params.keyword,
        'tag_ids': search_item_params.tag_ids,
    }
    se = SearchEngine(search_item_params.subject, EsItem, **params)
    se.filling()
    res = se.search()
    ret = []
    total = res.total
    for hit in res.hits:
        item_id = hit['_id']
        ret.append({'item_id': item_id,
                    'item_text': item2text(hit)})
    pprint(res.hits)
    return total, ret


