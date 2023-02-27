import json
import re
from pprint import pprint

import openai
import requests
openai.api_key = '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'

def askChatGPT(questions):
    prompt = questions
    model_engine = "text-davinci-003"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    msg = completions.choices[0].text
    print(msg)

askChatGPT("帮我写一个快速排序的样例")
# res = requests.post('http://localhost:8899/wx/test')
# print(res)
# raw = '<span class="math-tex" type="span">aabbaabababab</span>'
# res = re.sub(r'<span class="math-tex" type="span">(.*?)</span>', r'\1', raw)
# print(res, raw)
# url = 'http://10.8.27.125:7321/english/pub/papers/shougong_items?data=%7B%22appid%22:%2278bd03af%22,%22username%22:813510,%22sign%22:%22%22,%22customer_id%22:%22d86c65318b6a20202fe95b8873071b19%22,%22edu%22:3,%22suit_paper_id%22:%2260a5d3b2cb0f51548b4a661e%22%7D'
# req = requests.get(url)
# dt = json.loads(req.text)
# res = dt['data']['suit_paper']['parts'][0][31]['data']
# pprint(res)
