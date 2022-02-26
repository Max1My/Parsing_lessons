import requests
import json

url = 'https://api.instagram.com/oauth/authorize'
client_id = '437448591400882'
redirect_uri = 'http://89.108.81.6'
scope = 'user_profile,user_media'
response_type = 'code'
response = requests.get(url,params={client_id:client_id,redirect_uri:redirect_uri,scope:scope,response_type:response_type})
with open('result_auth_instagram.txt','w') as f:
    f.write(str(response))