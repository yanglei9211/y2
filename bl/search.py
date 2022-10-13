
from elasticsearch_dsl import Q, Search

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


