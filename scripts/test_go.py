import json
import time
from pprint import pprint

import requests

host = 'http://127.0.0.1:8888'

def get_item_detail():
    url = "{}/get_item_detail".format(host)
    data = {
        'subject': 'math',
        'item_id': '5f38a722770b515643ddd3bd'
    }
    res = requests.post(url, data)
    print(res.status_code)
    dt = json.loads(res.text)
    pprint(dt)

def sub_func():
    # url = "{}/sub?x=100000&y=7".format(host)
    url = "http://127.0.0.1:8888/sub?x=100000&y=7"
    # url = "http://127.0.0.1:8899/api/y2/test/sub?x=100000&y=7"
    data = {
        'x': 100000,
        'y': 7
    }
    st = time.time()
    res = requests.post(url, data)
    ed = time.time()
    print(res.status_code, (ed-st)*1000)
    dt = json.loads(res.text)
    pprint(dt)

sub_func()
