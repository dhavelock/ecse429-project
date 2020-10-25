import requests
import json

base_url = 'http://localhost:4567/'

def reset_system():
    res = requests.post(base_url + 'admin/data/thingifier')
    if res.status_code == 200:
        print("System data successfully cleared")
    else:
        raise Exception("System failed to reset")

def create_todo(body, headers={'Content-Type': 'application/json'}):
    res = requests.post(base_url + 'todos', headers=headers, data=json.dumps(body))
    return res.json()

def create_category(body, headers={'Content-Type': 'application/json'}):
    res = requests.post(base_url + 'categories', headers=headers, data=json.dumps(body))
    return res.json()

def create_project(body, headers={'Content-Type': 'application/json'}):
    res = requests.post(base_url + 'projects', headers=headers, data=json.dumps(body))
    return res.json()

def print_response(response):
    print('Status Code:', response.status_code)

    try:
        print('Body:', json.dumps(response.json(), indent=2))
    except:
        print('No Body')