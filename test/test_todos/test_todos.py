import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, print_response

url = 'http://localhost:4567/todos'
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
    assert len(res_body['todos']) == 0

def test_get_non_empty_response():

    # Given
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
    # assert res_todo1['doneStatus'] == todo1['doneStatus']
    assert res_todo1['description'] == todo1['description']
    assert res_todo2['title'] == todo2['title']
    # assert res_todo2['doneStatus'] == todo2['doneStatus']
    assert res_todo2['description'] == todo2['description']

def test_put_not_allowed():

    # When
    res = requests.put(url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_post_todo_valid_body():

    # Given
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
    # assert res_body['doneStatus'] == todo['doneStatus']
    assert res_body['description'] == todo['description']

def test_post_todo_invalid_body():
    # Given
    todo = {
        'doneStatus': False,
        'description': 'this is a description'
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(todo))
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