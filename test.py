import json

import requests

# res = requests.post('http://127.0.0.1:8888/login', headers={'Content-Type': 'application/json', 'username': '111111111111111111111111'}, data="{'username': '111', 'password': '111'}")
res = requests.get('http://127.0.0.1:8888/', headers={'Content-Type': 'application/json', 'username': '111111111111111111111111'}, data="{'username': '111', 'password': '111'}")
print(res.status_code)
print(res.raw.read())
