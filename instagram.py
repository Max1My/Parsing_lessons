import requests
import json

url = 'https://www.googleapis.com/youtube/v3'
response = requests.get(url)
print(response)