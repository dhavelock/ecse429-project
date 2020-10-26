import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, create_project, print_response, create_todo_project_relation
import xml.dom.minidom

base_url = 'http://localhost:4567/todos/'
project_url = 'http://localhost:4567/projects/'

def url(todo_id, project_id):
    return base_url + str(todo_id) + '/tasksof/' + str(project_id)

def setup_function(function):
    reset_system()

def teardown_function(function):
    pass

def test_get_todo_project_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    project = {
            'title': 'Office Work',
            'completed': False,
            'active': False,
            'description': 'a description'
    }

    project_id = create_project(project)['id']

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description',
        'tasksof': [
            {
                'id': project_id
            }
        ]
    }

    todo_id = create_todo(todo)['id']

    # When
    res = requests.get(url(todo_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_put_todo_project_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    project = {
            'title': 'Office Work',
            'completed': False,
            'active': False,
            'description': 'a description'
    }

    project_id = create_project(project)['id']

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description',
        'tasksof': [
            {
                'id': project_id
            }
        ]
    }

    todo_id = create_todo(todo)['id']

    # When
    res = requests.put(url(todo_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_post_todo_project_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    project = {
            'title': 'Office Work',
            'completed': False,
            'active': False,
            'description': 'a description'
    }

    project_id = create_project(project)['id']

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description',
        'tasksof': [
            {
                'id': project_id
            }
        ]
    }

    todo_id = create_todo(todo)['id']

    # When
    res = requests.post(url(todo_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_delete_todo_project():

    # Given
    headers = {'Content-Type': 'application/json' }

    project = {
            'title': 'Office Work',
            'completed': False,
            'active': False,
            'description': 'a description'
    }

    project_id = create_project(project)['id']

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description',
        'tasksof': [
            {
                'id': project_id
            }
        ]
    }

    todo_id = create_todo(todo)['id']

    create_todo_project_relation(todo_id, project_id)

    # When
    res = requests.delete(url(todo_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

    # Fetch todo and project to assert that the project relationship was deleted
    updated_todo = requests.get(base_url + todo_id, headers=headers)
    updated_todo_body = updated_todo.json()

    print('Todo:')
    print_response(updated_todo)

    assert updated_todo_body['todos'][0].get('tasksof') is None

    updated_project = requests.get(project_url + todo_id, headers=headers)
    updated_project_body = updated_project.json()

    print('Project:')
    print_response(updated_project)

    assert updated_project_body['projects'][0].get('tasks') is None

def test_delete_todo_project_relationship_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    project = {
            'title': 'Office Work',
            'completed': False,
            'active': False,
            'description': 'a description'
    }

    project_id = create_project(project)['id']

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    # When
    res = requests.delete(url(todo_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 404

def test_delete_todo_project_project_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    project_id = '999'

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    # When
    res = requests.delete(url(todo_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 404

def test_delete_todo_project_todo_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    project = {
            'title': 'Office Work',
            'completed': False,
            'active': False,
            'description': 'a description'
    }

    todo = {
        'title': 'todo title'
    }

    project_id = create_project(project)['id']

    todo_id = create_todo(todo)['id']

    create_todo_project_relation(todo_id, project_id)

    invalid_id = '999'

    # When
    res = requests.delete(url(invalid_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 400

def test_options_todo_project_ok():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.options(url(any_id, any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_head_todo_project_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.head(url(any_id, any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_patch_todo_project_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.patch(url(any_id, any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405
