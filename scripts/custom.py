from pprint import pprint

import requests

platform_host = "10.198.16.168:1889"
platform_group = "alps-hydra-test"
ditto_host = "http://10.198.21.134:1887/"
ditto_group = "test"
stage = "test"


def get_custom(school_id):
    # dubbo = DubboRPCService('com.voxlearning.platform.saas.service.dp.DPTenantLoader', '20221024')
    # res = dubbo.request('loadBySchoolId', [school_id])
    url = ditto_host
    data = {
        "interface": "com.voxlearning.platform.saas.service.dp.DPTenantLoader",
        "method": "loadBySchoolId",
        "group": ditto_group,
        "version": "20221024",
        "paramValues": [school_id]
    }
    rep = requests.post(url, json=data, timeout=5)
    res = rep.json()
    pprint(res)
    res = res['data']
    res = [str(r['customerId']) for r in res]
    return res


res = get_custom(4252)
