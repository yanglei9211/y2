import json
import os
import sys

from bson import ObjectId

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.es.item import EsItem
from model.es.suit_packet import EsPacket
from model.db_model.base_model import Item, SuitPacket


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

def update_packet(packet_ids, subject):
    sps = SuitPacket.find_by_ids(subject, [ObjectId(x) for x in packet_ids])
    for p in sps:
        print(p['_id'])
    es_packets = []
    for p in sps:
        print(p['_id'])
        es_p = {
            'suit_packet_id': str(p['_id']),
            'username': p.get('username','system'),
            'name': p['name'],
            'edu': p['edu'],
            'suit_papers': p['suit_papers'],
            'use_info': p.get('use_info', {}),
        }
        for i, s in enumerate(es_p['suit_papers']):
            es_p['suit_papers'][i]['suit_paper_id'] = str(es_p['suit_papers'][i]['suit_paper_id'])
        es_packets.append(es_p)
    EsPacket.update_many(subject, es_packets, refresh=False)

def create_idx():
    print(sys.path)
    for subject in [
        'math',
        # 'english',
        # 'chinese',
    ]:
        print("build item index")
        index_name = EsItem.create_index(subject)
        alias_name = EsItem.realias(subject, index_name)
        print(index_name, alias_name)
        print("build packet index")
        index_name = EsPacket.create_index(subject)
        alias_name = EsPacket.realias(subject, index_name)
        print(index_name, alias_name)


def update_items():
    print(sys.path)
    subject = 'math'
    item_ids = [
        # type= 1001
        "63d78cfb2ce3c42a9358b7f7",
        "63be52092ce3c42a94d5088c",
        "63bd32e3490a660001d90519",
        "63bd325d490a660001d90515",
        "63b7e419f2ec13000130fd87",
        "63b78e9e2ce3c4778ee7094b",
        "63b3f6a12ce3c431f8057abe",
        "63ac1fab65e47000012bf393",
        "63ac1f7265e47000012bf392",
        "63ac114d2ce3c446d8e5d62d",
        "63ac02982ce3c446d701c719",
        "63aaa0cf11d1b90001b7ce3e",
        "63aa626611d1b90001b7ce13",
        "63aa623b2ce3c446d8e5d5da",
        "63aa623b2ce3c446d8e5d5d9",
        "63aa623b2ce3c446d8e5d5d8",
        "63aa623b2ce3c446d8e5d5d7",
        "63aa623b2ce3c446d8e5d5d6",
        "63aa598b11d1b90001b7cdf9",
        "63aa58942ce3c446d701c6cc",
        
        
        
        # tpye=1003
        "616f8ab2d6b0c1cafe9d4b78",
    "58c0f5c7def2976456dc83de",
    "59561aa1def29748b0df486b",
    "571db0aedef297635ff914e8",
    "5875da41def2971470586744",
    "57a3eb60def297386242fcdb",
    "55f8c6a45417d169d8ff7395",
    "56f105745417d15b16270760",
    "57a3e9c4def297386242fcd1",
    "5599f87b5417d1251ce27543",
    "56f101c15417d15b3ead7086",
    "57a3ebe9def297386242fce0",
    "57035b035417d166b6d4cca8",
    "56aed29b5417d10c1373a377",
    "55a5f82c5417d147b19c07d3",
    "5666856f5417d16f0c6d373e",
    "5664ec4d5417d16f0c6d3600",
    "543b74890045fe48f837325b",
    "544ef1e40045fe48ff6f7dfd",
    "54197b230045fe0569296427",
    "54197a6f0045fe05692963a2",
    "5445f3590045fe487b37fd06",
    "58e7784fdef2972c5e74493b",
    "592e8869def29709af351e6d",
    "576a0914def2976fbfe5bf08",
    "5932abebdef29758fe378c21",
    "59631195def297723ddf1a1b",
    "59631224def2977262be5f00",
    "5764ad2bdef297303ae13524",
    "57639f8adef297303ae13409",
    "5947e847def297347af8d51f",
    "5932b72fdef29759238d54c2",
    "59a82781def29730720e49d5",
    "593feb8bdef2976f74178105",
    "59105e4cdef297409c94a69a",
    "5952578ddef29747b2927090",
    "5948a8d5def297347af8d553",
    "595f8ca1def2971122fa1760",
    "58beda28def2973120110547",
    "59450e7cdef297347af8d0f0",
    "5970734adef2971c81de4fc2",
    "586361fedef2970bdef41e60",
    "57a403e8def2976a3f2c2097",
    "58cd54fcdef2976bd25277d1",
    "59451204def297347af8d16e",
    "5932a972def297584571b024",
    "593ffccedef2976f71821f59",
    "59b6757fdef2971812e5931c",
    "57a43e65def2973861e99922",
    "58948ca0def29768c05b3218",
    "5895aeecdef297087c6597ec",
    "58cbfdbbdef2976bd3dfaec9",
    "5911883adef2973fe3ebe00b",
    "58ed7c99def29738822b8ed4",
    "594132cddef29715110d3eb1",
    "5900997bdef2976ee309e595",
    "596f6bcadef2971c5cd1e71d",
    "5984283ddef29778360764d5",
    "595614dddef297480c1142c0",
    "59706371def2971c12b2ebf1",
    "59645b12def29772182892c2",
    "58db56aedef29777e30ffdcc",
    "58db671cdef29777e26000fd",
    "58859507def297521b5ed3f6",
    "58636b5ddef2970bdef41e8a",
    "589bf826def29760b9a8e080",
    "58b262dcdef29721d60f7040",
    "59412724def2970b825bf2d9",
    "59400897def2976f7255c659",
    "593ff867def2976f73264ef9",
    "59782383def29772497f2895",
    "5989c2bedef2976fe2aa240c",
    "59842347def29778119a0a0a",
    "59659cf0def29771f3181335",
    "571db08fdef297635ff914db",
    "57a40117def2973861e99847",
    "58830467def297734684668c",
    "588818e1def29708cf7035d2",
    "5885920ddef297521b5ed3da",
    "58c269a3def29738296c28f6",
    "57a43013def2976a3f2c20ca",
    "58d4d111def29757c192fd33",
    "58d521e1def2975f9ae2396f",
    "58b5606edef2972a48e1a81e",
    "5894768fdef297613723dd72",
    "5947ea7bdef2973455fac9de",
    "596f3ec7def2971c81de4cb1",
    "5960490bdef2971122fa17c2",
    "57349133def29734eb9145b9",
    "57a40111def297386242fd8f",
    "5875d456def297147058672a",
    "58859436def297521b5ed3ef",
    "588818e1def29708cf7035d3",
    "589d16efdef2970777760084",
    "571db161def297635ff91508",
    "5896f05adef2971a26f98e4d",
    "58b38321def297228e7e15e8",
    "58c0fbc1def2977d41c76df1",
    "578dab89def2976a3f2c199b",
    "58c7bb4bdef297405bb200f9",
        # type= 1002
        "63d7ac5f2ce3c42a9358b805",
        "63d790147989180001434f15",
        "63d78cfb2ce3c42a9358b7f8",
        "63c102390538430001879cdf",
        "63c1012d0538430001879cd3",
        "63c100f20538430001879ccf",
        "63b78ea62ce3c4778dafa4ff",
        "63b4f1a82ce3c4778dafa4b0",
        "63b40a1722a391b379cb0bfb",
        "63b4072a22a391b379cb0bf9",
        # type= 1003
        "63d78cfb2ce3c42a9358b7ff",
        "63d78cfb2ce3c42a9358b7fe",
        "63d78cfb2ce3c42a9358b7fd",
        "63d78cfb2ce3c42a9358b7fc",
        "63d78cfb2ce3c42a9358b7fb",
        "63d78cfb2ce3c42a9358b7fa",
        "63ac114d2ce3c446d8e5d62f",
        "63ac02982ce3c446d701c71b",
        "63aa623b2ce3c446d8e5d5e2",
        "63aa623b2ce3c446d8e5d5e1",

    ]
    update_item(item_ids, subject)


def update_packets():
    print(sys.path)
    subject = 'math'
    packet_ids = [
        '5f801f4284da5a2834fa6f90',
        '5fdac70fea93710b2626da87',
        '5f6c18ba84da5a37fc6919d8',
        '5fdacada72a3165f0c1f60c5',
        '62b9626a2ce3c412dfc9856d',
        '62b99c482ce3c447ef8fbb2c',
        '62bc0c272ce3c42989eac56a',
        '62c40f65bb2e398c3c8b020a',
        '63575273c9cef683885706e3',
        '636486617bbbcab0101802ac',
        '63bf79c02f16f6b0efb7b18f',
        '63be524b1003360a6a21a914',
        '63be240da65f8f663e052eb6',
        '63bd2c6da65f8f663e052eb0',
        '63bbe0f37ae647898d449da2',
    ]
    update_packet(packet_ids, subject)

if __name__ == '__main__':
    update_items()
    # create_idx()
    # update_packets()
