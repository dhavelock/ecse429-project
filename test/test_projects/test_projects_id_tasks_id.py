import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, create_project, create_category, print_response
import xml.dom.minidom

url = 'http://localhost:4567/projects/'
headers = {'Content-Type': 'application/json' }

def setup_function(function):
    reset_system()

def teardown_function(function):
    pass

def test_get_project_id_tasks_id_not_allowed():

    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']

    project = {
        'title': 'Project title',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project_id = create_project(project)['id']

    # When
    res = requests.get(url + project_id + '/tasks/' + todo_id, headers=headers)
    print_response(res)
    # Then
    #THIS DOESNT FOLLOW THE DOCUMENTATION - A PROBLEM
    assert res.status_code == 404

def test_put_project_id_tasks_id_not_allowed():

    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']

    project = {
        'title': 'Project title',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project_id = create_project(project)['id']

    # When
    res = requests.put(url + project_id + '/tasks/' + todo_id, headers=headers)
    print_response(res)
    # Then
    assert res.status_code == 405

def test_post_project_id_tasks_id_not_allowed():

    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']

    project = {
        'title': 'Project title',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project_id = create_project(project)['id']

    # When
    res = requests.post(url + project_id + '/tasks/' + todo_id, headers=headers)
    print_response(res)
    # Then
    # THIS IS A PROBLEM - NOT ACCURATE IN THE SWAGGER FILE SHOULD BE 405
    assert res.status_code == 404


def test_delete_project_id_tasks_id_allowed():

    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']

    project = {
        'title': 'Project title',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project_id = create_project(project)['id']

    todo_to_add = {
        'ID': todo_id
    }

    project_id = create_project(project)['id']

    res = requests.post(url + project_id + '/tasks', headers=headers, data=json.dumps(todo_to_add))
    
    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()

    assert len(res_body['projects'][0]) == 6

    print_response(res)
    # When
    res = requests.delete(url + project_id + '/tasks/' + todo_id, headers=headers)

    assert res.status_code == 200

    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()
    print_response(res)

    assert len(res_body['projects'][0]) == 5


def test_delete_project_id_tasks_id_invalid_project():

    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']

    project = {
        'title': 'Project title',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project_id = create_project(project)['id']
    invalid_project_id = int(project_id) + 1

    todo_to_add = {
        'ID': todo_id
    }

    # Create project/category relationship

    res = requests.post(url + project_id + '/tasks', headers=headers, data=json.dumps(todo_to_add))
    
    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()

    # When
    res = requests.delete(url + str(invalid_project_id) + '/tasks/' + todo_id, headers=headers)

    assert res.status_code == 400

    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()
    print_response(res)

    # assert relationship wasn't deleted
    assert len(res_body['projects'][0]) == 6
    assert res_body['projects'][0]['tasks'][0]['id'] == todo_id

def test_delete_project_id_tasks_id_invalid_todo():

    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']
    invalid_todo_id = int(todo_id) + 1


    project = {
        'title': 'Project title',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project_id = create_project(project)['id']

    todo_to_add = {
        'ID': todo_id
    }

    project_id = create_project(project)['id']

    # Create project/category relationship

    res = requests.post(url + project_id + '/tasks', headers=headers, data=json.dumps(todo_to_add))
    
    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()

    # When
    res = requests.delete(url + project_id + '/tasks/' + str(invalid_todo_id), headers=headers)
    res_body = res.json()
    print_response(res)

    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find any instances with projects/' + project_id + '/tasks/' + str(invalid_todo_id)


    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()
    print_response(res)

    # assert relationship wasn't deleted
    assert len(res_body['projects'][0]) == 6
    assert res_body['projects'][0]['tasks'][0]['id'] == todo_id

def test_project_id_tasks_id_options_OK():

    headers = {'Content-Type': 'application/json' }

    any_id ='999'

    # When
    res = requests.options(url + any_id + '/tasks/' + any_id, headers=headers)

    assert res.status_code == 200

def test_project_id_tasks_id_head_not_allowed():

    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.head(url + any_id + '/tasks/' + any_id, headers=headers)

    # THIS IS WRONG - IT SHOULD BE 405 ?
    assert res.status_code == 404

def test_project_id_tasks_id_patch_not_allowed():

    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.patch(url + any_id + '/tasks/' + any_id, headers=headers)

    assert res.status_code == 405