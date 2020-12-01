import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, print_response, create_project, create_category
import xml.dom.minidom

url = 'http://localhost:4567/todos'
base_url = 'http://localhost:4567/'

def setup_function(function):
    reset_system()
    headers = dict()
    headers = {'Content-Type': 'application/json'} 


def test_get_empty_response():

    # Given
    headers = {'Content-Type': 'application/json' } 

    # When
    res = requests.get(url, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['todos']) == 0

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
    headers = {'Content-Type': 'application/json' } 

    todo1 = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo2 = {
        'title': 'Task title 2',
        'doneStatus': True,
        'description': 'this is another description'
    }

    create_todo(todo1)
    create_todo(todo2)

    # When
    res = requests.get(url, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['todos']) == 2

    # Get todos from list since there is no guarantee on ordering in the response
    res_todo1 = [todo for todo in res_body['todos'] if todo['title'] == todo1['title']][0]
    res_todo2 = [todo for todo in res_body['todos'] if todo['title'] == todo2['title']][0]

    assert res_todo1['title'] == todo1['title']
    assert res_todo1['doneStatus'] == str(todo1['doneStatus']).lower()
    assert res_todo1['description'] == todo1['description']
    assert res_todo2['title'] == todo2['title']
    assert res_todo2['doneStatus'] == str(todo2['doneStatus']).lower()
    assert res_todo2['description'] == todo2['description']

def test_get_non_empty_response_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml' } 
    
    todo1 = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo2 = {
        'title': 'Task title 2',
        'doneStatus': True,
        'description': 'this is another description'
    }

    create_todo(todo1)
    create_todo(todo2)

    # When
    res = requests.get(url, headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

def test_put_not_allowed():

    # When
    res = requests.put(url, headers={'Content-Type': 'application/json'} )

    # Then
    print_response(res)

    assert res.status_code == 405

def test_post_todo_valid_body():

    # Given
    headers = {'Content-Type': 'application/json' } 

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(todo))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == todo['title']
    assert res_body['doneStatus'] == str(todo['doneStatus']).lower()
    assert res_body['description'] == todo['description']

def test_post_todo_valid_body_with_project_relationship():

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

    # When
    res = requests.post(url, headers=headers, data=json.dumps(todo))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == todo['title']
    assert res_body['doneStatus'] == str(todo['doneStatus']).lower()
    assert res_body['description'] == todo['description']

    # Assert todo was added to project
    updated_project = requests.get(base_url + 'projects/' + project_id, headers=headers)
    updated_project_body = updated_project.json()

    print_response(updated_project)
    assert updated_project_body['projects'][0]['tasks'][0]['id'] == res_body['id']

def test_post_todo_valid_body_with_category_relationship():

    # Given
    headers = {'Content-Type': 'application/json' } 

    category = {
        'title': 'category title',
        'description': 'description of category'
    }

    category_id = create_category(category)['id']

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description',
        'categories': [
            {
                'id': category_id
            }
        ]
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(todo))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == todo['title']
    assert res_body['doneStatus'] == str(todo['doneStatus']).lower()
    assert res_body['description'] == todo['description']
    assert res_body['categories'][0]['id'] == category_id

    # Assert todo was added to category
    updated_category = requests.get(base_url + 'categories/' + category_id, headers=headers)
    updated_category_body = updated_category.json()

    print_response(updated_category)
    assert updated_category_body['categories'][0]['todos'][0]['id'] == res_body['id']

def test_post_todo_valid_body_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'} 

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(todo))

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 201

def test_post_todo_invalid_body():

    # Given
    headers = {'Content-Type': 'application/json' } 

    todo = {
        'doneStatus': False,
        'description': 'this is a description'
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(todo))

    # Then
    print_response(res)

    assert res.status_code == 400

def test_delete_not_allowed():

    # When
    res = requests.delete(url, headers={'Content-Type': 'application/json' } )

    # Then
    print_response(res)

    assert res.status_code == 405

def test_options_ok():

    # When
    res = requests.options(url, headers={'Content-Type': 'application/json' } )

    # Then
    print_response(res)

    assert res.status_code == 200

def test_head_ok():

    # When
    res = requests.head(url, headers={'Content-Type': 'application/json' } )

    # Then
    print_response(res)

    assert res.status_code == 200

def test_patch_not_allowed():

    # When
    res = requests.patch(url, headers={'Content-Type': 'application/json' } )

    # Then
    print_response(res)

    assert res.status_code == 405