import requests
import json

def reset_system():
    res = requests.post('http://localhost:4567/admin/data/thingifier')
    if res.status_code == 200:
        print("System data successfully cleared")
    else:
        raise Exception("System failed to reset")

def hello():
    print('hello')