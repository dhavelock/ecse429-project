import requests
import json

base_url = 'http://localhost:4567/'


def reset_system():
    headers={'Content-Type': 'application/json'}

    res = requests.post(base_url + 'admin/data/thingifier')
    if res.status_code == 200:
        print('System data successfully cleared')
    else:
        raise Exception('System failed to reset')

    # Check that no todos, projects, or categories are present
    res = requests.get(base_url + 'todos', headers)
    assert len(res.json()['todos']) == 0

    res = requests.get(base_url + 'projects', headers)
    assert len(res.json()['projects']) == 0

    res = requests.get(base_url + 'categories', headers)
    assert len(res.json()['categories']) == 0

    print('System is cleared of all todos, projects, and categories')


def create_todo(body, headers={'Content-Type': 'application/json'}):
    res = requests.post(base_url + 'todos', headers=headers,
                        data=json.dumps(body))
    return res.json()


def create_category(body, headers={'Content-Type': 'application/json'}):
    res = requests.post(base_url + 'categories',
                        headers=headers, data=json.dumps(body))
    return res.json()


def create_project(body, headers={'Content-Type': 'application/json'}):
    res = requests.post(base_url + 'projects',
                        headers=headers, data=json.dumps(body))
    return res.json()


def create_todo_category_relation(todo_id, category_id):
    headers = {'Content-Type': 'application/json'}
    requests.post(base_url + 'todos/' + str(todo_id) + '/categories',
                  headers=headers, data=json.dumps({'id': category_id}))
    requests.post(base_url + 'categories/' + str(category_id) +
                  '/todos', headers=headers, data=json.dumps({'id': todo_id}))


def create_todo_project_relation(todo_id, project_id):
    headers = {'Content-Type': 'application/json'}
    requests.post(base_url + 'todos/' + str(todo_id) + '/tasksof',
                  headers=headers, data=json.dumps({'id': project_id}))
    requests.post(base_url + 'projects/' + str(project_id) +
                  '/tasks', headers=headers, data=json.dumps({'id': todo_id}))


def create_category_project_relation(category_id, project_id):
    headers = {'Content-Type': 'application/json'}
    requests.post(base_url + 'categories/' + str(category_id) +
                  '/projects', headers=headers, data=json.dumps({'id': project_id}))
    requests.post(base_url + 'projects/' + str(project_id) + '/categories',
                  headers=headers, data=json.dumps({'id': category_id}))


def delete_project(project_id):
    headers = {'Content-Type': 'application/json'}
    res = requests.delete(base_url + 'projects/' + project_id, headers=headers)

    return res


def get_project(project_id):
    headers = {'Content-Type': 'application/json'}
    res = requests.get(base_url + 'projects/' + project_id, headers=headers)

    return res


def get_projects(params={}):
    headers = {'Content-Type': 'application/json'}
    res = requests.get(base_url + 'projects', headers=headers, params=params)

    return res


def get_todos(params={}):
    headers = {'Content-Type': 'application/json'}
    res = requests.get(base_url + 'todos', headers=headers, params=params)

    return res


def get_project_tasks(project_id, params={}):
    headers = {'Content-Type': 'application/json'}
    res = requests.get(base_url + 'projects/' + project_id + '/tasks', headers=headers, params=params)

    return res


def print_response(response):
    print('Request:')
    print(response.request.method, response.request.url)
    print('Headers:', response.request.headers)
    print('Body:', response.request.body)
    print()

    print('Response:')
    print('Status Code:', response.status_code)

    try:
        print('Body:', json.dumps(response.json(), indent=2))
    except:
        print('No Body')
