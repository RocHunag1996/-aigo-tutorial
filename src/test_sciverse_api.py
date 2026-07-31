import os, requests, json

API_KEY = os.environ.get('SCIVERSE_API_KEY', '')
assert API_KEY, '请先设置 SCIVERSE_API_KEY 环境变量'

resp = requests.post(
    'https://api.sciverse.space/meta-search',
    headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
    json={'query': 'lithium ion battery cathode', 'page': 1, 'page_size': 3},
    timeout=30,
)
print(json.dumps(resp.json(), ensure_ascii=False, indent=2)[:2000])
