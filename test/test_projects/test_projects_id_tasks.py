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

def test_get_project_empty_tasks():

    # Given
    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project_id = create_project(project)['id']

    specific_project_id_url = url + project_id

    # When
    res = requests.get(specific_project_id_url + '/tasks', headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['todos']) == 0

def test_get_project_with_tasks():

    # Given
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
        'description': 'agna aliqua. Ut enim abc',
        'tasks': [
            {
                'id': todo_id
            }
        ]
    }

    project_id = create_project(project)['id']

    # When
    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()

    print_response(res)

    # Then
    assert res.status_code == 200
    assert res_body['projects'][0]['tasks'][0]['id'] == todo_id
    assert len(res_body['projects'][0]['tasks'][0]) == 1

def test_get_project_with_tasks_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'} 
    
    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']

    project = {
        'title': 'Project title',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc',
        'tasks': [
            {
                'id': todo_id
            }
        ]
    }

    project_id = create_project(project)['id']

    # When
    res = requests.get(url + project_id + '/tasks', headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

def test_put_project_id_tasks_not_allowed():

    # Given
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

    todo_to_add = {
        'ID': todo_id
    }

    project_id = create_project(project)['id']

    # When
    res = requests.put(url + project_id + '/tasks', headers=headers, data=json.dumps(todo_to_add))
    
    # Then
    print_response(res)
    assert res.status_code == 405

def test_post_project_id_tasks():

    # Given
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

    todo_to_add = {
        'ID': todo_id
    }

    project_id = create_project(project)['id']

    # When
    res = requests.post(url + project_id + '/tasks', headers=headers, data=json.dumps(todo_to_add))
    
    # Then
    print_response(res)
    assert res.status_code == 201

    # Confirm it was succesfully created from both project and todo
    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()

    print_response(res)
    assert res_body['projects'][0]['tasks'][0]['id'] == todo_id

    res = requests.get('http://localhost:4567/todos/' + todo_id, headers=headers)
    res_body = res.json()

    print_response(res)
    assert res_body['todos'][0]['tasksof'][0]['id'] == project_id

def test_post_project_id_tasks_invalid_project_id():

    # Given
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

    todo_to_add = {
        'ID': todo_id
    }

    project_id = create_project(project)['id']
    invalid_project_id = int(project_id) + 1

    # When
    res = requests.post(url + str(invalid_project_id) + '/tasks', headers=headers, data=json.dumps(todo_to_add))
    res_body = res.json()
    
    # Then
    print_response(res)
    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find parent thing for relationship projects/' + str(invalid_project_id) + '/tasks'

def test_post_project_id_tasks_invalid_todo_id():

    # Given
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

    todo_to_add = {
        'ID': str(invalid_todo_id)
    }

    project_id = create_project(project)['id']

    # When
    res = requests.post(url + project_id + '/tasks', headers=headers, data=json.dumps(todo_to_add))
    res_body = res.json()
   
    # Then
    print_response(res)
    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find thing matching value for ID'

def test_delete_project_id_tasks():

    # Given
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

    todo_to_add = {
        'ID': todo_id
    }

    project_id = create_project(project)['id']

    # When
    res = requests.delete(url + project_id + '/tasks', headers=headers, data=json.dumps(todo_to_add))
    
    # Then
    print_response(res)
    assert res.status_code == 405

def test_project_id_tasks_options_OK():

    # Given
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

    todo_to_add = {
        'ID': todo_id
    }

    project_id = create_project(project)['id']

    # When
    res = requests.options(url + project_id + '/tasks', headers=headers, data=json.dumps(todo_to_add))

    # Then
    print_response(res)
    assert res.status_code == 200

def test_project_id_tasks_head_OK():

    # Given
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

    todo_to_add = {
        'ID': todo_id
    }

    project_id = create_project(project)['id']

    # When
    res = requests.head(url + project_id + '/tasks', headers=headers, data=json.dumps(todo_to_add))

    # Then
    print_response(res)
    assert res.status_code == 200

def test_project_id_tasks_patch_not_allowed():

    # Given
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

    todo_to_add = {
        'ID': todo_id
    }

    project_id = create_project(project)['id']

    # When
    res = requests.patch(url + project_id + '/tasks', headers=headers, data=json.dumps(todo_to_add))

    # Then
    print_response(res)
    assert res.status_code == 405