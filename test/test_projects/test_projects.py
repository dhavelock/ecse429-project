import pytest
import requests
import json
from test.common.helper import reset_system, create_project, print_response, create_todo, create_category
import xml.dom.minidom

url = 'http://localhost:4567/projects'
base_url = 'http://localhost:4567/'
headers = {'Content-Type': 'application/json' } 

def setup_function(function):
    reset_system()

def teardown_function(function):
    pass

def test_get_empty_response():

    # When
    res = requests.get(url, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['projects']) == 0

def test_get_empty_response_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml' } 

    # When
    res = requests.get(url, headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

def test_get_non_empty_response():

    # Given
    project1 = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project2 = {
        'title': 'Project title 2',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim xyz'
    }

    create_project(project1)
    create_project(project2)

    # When
    res = requests.get(url, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['projects']) == 2

    # Get todos from list since there is no guarantee on ordering in the response
    res_project1 = [project for project in res_body['projects'] if project['title'] == project1['title']][0]
    res_project2 = [project for project in res_body['projects'] if project['title'] == project2['title']][0]

    assert res_project1['title'] == project1['title']
    assert res_project1['description'] == project1['description']
    assert res_project2['title'] == project2['title']
    assert res_project2['description'] == project2['description']

def test_get_non_empty_response_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml' } 
    
    # Given
    project1 = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project2 = {
        'title': 'Project title 2',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim xyz'
    }

    create_project(project1)
    create_project(project2)

    # When
    res = requests.get(url, headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

def test_project_put_not_allowed():

    # When
    res = requests.put(url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_post_project_valid_body():

    # Given
    project = {
        'title': 'Project title x',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim xyz'
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(project))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == project['title']
    assert res_body['description'] == project['description']

def test_post_project_valid_body_with_todo_relation():

    # Given
    todo = {
        'title': 'todo title'
    }

    todo_id = create_todo(todo)['id']

    project = {
        'title': 'Project title x',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim xyz',
        'tasks': [
            {
                'id': todo_id
            }
        ]
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(project))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == project['title']
    assert res_body['description'] == project['description']
    assert res_body['tasks'][0]['id'] == todo_id

    # Assert project was added to todo
    updated_todo = requests.get(base_url + 'todos/' + todo_id, headers=headers)
    updated_todo_body = updated_todo.json()

    print_response(updated_todo)
    assert updated_todo_body['todos'][0]['tasksof'][0]['id'] == res_body['id']

def test_post_project_valid_body_with_category_relation():

    # Given
    category = {
        'title': 'category title',
        'description': 'description of category'
    }

    category_id = create_category(category)['id']

    project = {
        'title': 'Project title x',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim xyz',
        'categories': [
            {
                'id': category_id
            }
        ]
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(project))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == project['title']
    assert res_body['description'] == project['description']
    assert res_body['categories'][0]['id'] == category_id

    # Assert project was added to category
    updated_category = requests.get(base_url + 'categories/' + category_id, headers=headers)
    updated_category_body = updated_category.json()

    print_response(updated_category)
    assert updated_category_body['categories'][0]['projects'][0]['id'] == res_body['id']

def test_post_project_valid_body_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'} 

    project = {
        'title': 'Project title x',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim xyz'
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(project))

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 201

def test_post_project_invalid_body():
    
    # Given
    project = {
        'id': 1
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(project))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 400

def test_delete_not_allowed():

    # When
    res = requests.delete(url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_options_ok():

    # When
    res = requests.options(url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_head_ok():

    # When
    res = requests.head(url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_patch_not_allowed():

    # When
    res = requests.patch(url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405