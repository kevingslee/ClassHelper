import requests

BASE = "http://192.168.1.176:5000/"

response = requests.post(BASE + "studentdata/geonhun/112")
print(response.json())
