import os
import sys
sys.path.append(os.path.abspath("."))
import json
from pprint import pprint

from model.db_model.redis import RedisClient, get_cache

f, rs = get_cache('63d8d0287989180001434ffa')
d = json.loads(rs)
pprint(d)
