import requests
import json

url = 'https://api.github.com/users/Max1My/repos'
response = requests.get(url)
for name in response.json():
    if name['name']:
        print(name['name'])
    with open('repos_list.json','a') as f:
        json.dump(name['name'],f)
