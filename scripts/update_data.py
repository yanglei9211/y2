import json
import os
import sys

from bson import ObjectId

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.es.item import EsItem
from model.db_model.base_model import Item

def update_item(item_ids, subject):
    items = Item.find_by_ids(subject, [ObjectId(x) for x in item_ids])
    for it in items:
        print(it['_id'])
    # raise Exception("stop")

    es_items = []
    for it in items:
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
        es_items.append(es_item)
    EsItem.update_many(subject, es_items, refresh=False)




def create_idx():
    print(sys.path)
    for subject in [
        'math',
        # 'english',
        # 'chinese',
    ]:
        index_name = EsItem.create_index(subject)
        print(index_name)
        alias_name = EsItem.realias(subject, index_name)
        print(alias_name)


def update_items():
    print(sys.path)
    subject = 'math'
    item_ids = [
        '5f3b66a7770b515908eee38d',
        '5d8b2d84cb0f514587467943',
        '5f892f2c770b514f672d7e31',
        '5d89cdb6cb0f51458745b830',
        '59394e41def29722d71b932d',
        '59111862def297409c94a756',
        '58ff50cddef2976f9b79b695',
        '576d1d28def2976fbfe5c577',
        '546025ce0045fe78c17c2c6c',
        '53ec3323e1382317a62def6b',
        '593fead0def2976f71821f12',
        '5b14e5b3def2977f28826d87',
    ]
    update_item(item_ids, subject)

if __name__ == '__main__':
    update_items()
    # create_idx()
