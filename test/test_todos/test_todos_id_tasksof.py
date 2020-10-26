import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, create_project, print_response
import xml.dom.minidom

base_url = 'http://localhost:4567/todos/'
projects_url = 'http://localhost:4567/projects/'

def url(id):
    return base_url + str(id) + '/tasksof'

def setup_function(function):
    reset_system()

def teardown_function(function):
    pass

def test_get_todos_projects():

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
    res = requests.get(url(todo_id), headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['projects'][0]['id'] == project_id
    assert res_body['projects'][0]['title'] == project['title']
    assert res_body['projects'][0]['completed'] == str(project['completed']).lower()
    assert res_body['projects'][0]['active'] == str(project['active']).lower()
    assert res_body['projects'][0]['description'] == project['description']
    assert res_body['projects'][0]['tasks'][0]['id'] == todo_id

def test_get_todos_projects_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

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
    res = requests.get(url(todo_id), headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

def test_get_todos_projects_todo_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    invalid_id = '999'

    # When
    res = requests.get(url(invalid_id), headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['todos']) == 0

def test_put_todos_projects_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.put(url(any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_post_todos_projects():

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

    body = {
        'id': project_id
    }

    # When
    res = requests.post(url(todo_id), headers=headers, data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 201

    # Fetch todo and project to assert tasksof relationship was created
    updated_todo = requests.get(base_url + todo_id, headers=headers)
    updated_todo_body = updated_todo.json()
    print_response(updated_todo)

    assert updated_todo_body['todos'][0]['tasksof'][0]['id'] == project_id

    updated_project = requests.get(projects_url + project_id, headers=headers)
    updated_project_body = updated_project.json()
    print_response(updated_project)

    assert updated_project_body['projects'][0]['tasks'][0]['id'] == todo_id

def test_post_todos_projects_invalid_body():

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

    body = {
        'idd': project_id
    }

    # When
    res = requests.post(url(todo_id), headers=headers, data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 400

# Undocumented
def test_post_todos_projects_todo_project_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    invalid_id = '999'

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    body = {
        'id': invalid_id
    }

    # When
    res = requests.post(url(todo_id), headers=headers, data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 404

# Undocumented
def test_post_todos_projects_todo_todo_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    invalid_id = '999'

    body = {
        'id': invalid_id
    }

    # When
    res = requests.post(url(invalid_id), headers=headers, data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 404

def test_delete_todos_projects_not_allowed():

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
    res = requests.delete(url(todo_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_options_todos_projects_ok():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.options(url(any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_head_todos_projects_ok():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.head(url(any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_patch_todos_projects_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.patch(url(any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405