import hashlib

from jose import jwt
from jose.constants import ALGORITHMS
from datetime import datetime, timedelta
SECRET_KEY = '2b86859545fe0a0ebff810fae597f60840c14e1b'

def gen_key():
    hstr = 'lei.yang|y2'
    hstr = hstr.encode('utf8')
    k = hashlib.sha1(hstr).hexdigest()
    print(k)

def encode():
    cur_time = datetime.utcnow()
    expire = datetime.utcnow() + timedelta(seconds=30)
    print(cur_time, expire)
    data = {
        'username': 'admin',
        'x': 1,
        'y': 2,
        'z': 3,
        'exp': expire,
    }
    print(data, SECRET_KEY, ALGORITHMS.HS256)
    token = jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHMS.HS256)
    print(token)


def decode():
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwieCI6MSwieSI6MiwieiI6MywiZXhwIjoxNjUxMzkyODI5fQ.bqxdnBY-6V8T95pfkc8sHERHYpDdaoEGGE7fU3j8ks0'
    pyload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHMS.HS256)
    print(pyload)


if __name__ == '__main__':
    # encode()
    decode()
    # expire = datetime.utcnow() + timedelta(seconds=int(128))
    # print(expire)