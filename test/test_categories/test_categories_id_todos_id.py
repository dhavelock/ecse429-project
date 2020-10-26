import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, create_category, print_response, create_todo_category_relation
import xml.dom.minidom

url = 'http://localhost:4567/categories/'
headers = {'Content-Type': 'application/json'}


def setup_function(function):
    reset_system()


def teardown_function(function):
    pass


def test_get_category_id_todos_id_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']

    category = {
        'title': 'category title',
        'description': 'a description',
        'todos': [
            {
                'id': todo_id
            }
        ]
    }

    category_id = create_category(category)['id']

    # When
    res = requests.get(url + category_id + '/todos/' +
                       todo_id, headers=headers)

    # Then
    print_response(res)
    assert res.status_code == 405


def test_put_category_id_todos_id_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']

    category = {
        'title': 'category title',
        'description': 'a description',
        'todos': [
            {
                'id': todo_id
            }
        ]
    }

    category_id = create_category(category)['id']

    # When
    res = requests.put(url + category_id + '/todos/' +
                       todo_id, headers=headers)

    # Then
    print_response(res)
    assert res.status_code == 405


def test_post_category_id_todos_id_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']

    category = {
        'title': 'category title',
        'description': 'a description'
    }

    category_id = create_category(category)['id']

    # When
    res = requests.post(url + category_id + '/todos/' +
                        todo_id, headers=headers)

    # Then
    print_response(res)
    assert res.status_code == 405


def test_delete_category_id_todos_id_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']

    category = {
        'title': 'category title',
        'description': 'a description',
        'todos': [
            {
                'id': todo_id
            }
        ]
    }

    category_id = create_category(category)['id']

    # When
    res = requests.delete(url + category_id + '/todos/' +
                          todo_id, headers=headers)

    # Then
    assert res.status_code == 200

    # When
    # Confirm it was succesfully deleted
    res = requests.get('http://localhost:4567/categories/' +
                       category_id, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)
    assert len(res_body['categories'][0]) == 3


def test_delete_category_id_todos_id_invalid_category():

    # Given
    headers = {'Content-Type': 'application/json'}

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']

    category = {
        'title': 'category title',
        'description': 'a description',
        'todos': [
            {
                'id': todo_id
            }
        ]
    }

    category_id = create_category(category)['id']
    invalid_category_id = int(category_id) + 1

    # When
    res = requests.delete(url + str(invalid_category_id) +
                          '/todos/' + todo_id, headers=headers)

    # Then
    assert res.status_code == 400

    # When
    res = requests.get('http://localhost:4567/categories/' +
                       category_id, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)
    # assert relationship wasn't deleted
    assert len(res_body['categories'][0]) == 4
    assert res_body['categories'][0]['todos'][0]['id'] == todo_id


def test_delete_category_id_todos_id_invalid_todo():

    # Given
    headers = {'Content-Type': 'application/json'}

    todo = {
        'title': 'todo title',
        'description': 'description of todo'
    }

    todo_id = create_todo(todo)['id']
    invalid_todo_id = int(todo_id) + 1

    category = {
        'title': 'category title',
        'description': 'a description',
        'todos': [
            {
                'id': todo_id
            }
        ]
    }

    category_id = create_category(category)['id']

    # When
    res = requests.delete(url + category_id + '/todos/' +
                          str(invalid_todo_id), headers=headers)
    res_body = res.json()

    # Then
    print_response(res)
    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find any instances with categories/' + \
        category_id + '/todos/' + str(invalid_todo_id)

    res = requests.get('http://localhost:4567/categories/' +
                       category_id, headers=headers)
    res_body = res.json()

    print_response(res)
    # assert relationship wasn't deleted
    assert len(res_body['categories'][0]) == 4
    assert res_body['categories'][0]['todos'][0]['id'] == todo_id


def test_category_id_todos_id_options_OK():

    # Given
    headers = {'Content-Type': 'application/json'}

    any_id = '999'

    # When
    res = requests.options(url + any_id + '/todos/' + any_id, headers=headers)

    # Then
    print_response(res)
    assert res.status_code == 200


def test_category_id_todos_id_head_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    any_id = '999'

    # When
    res = requests.head(url + any_id + '/todos/' + any_id, headers=headers)

    # Then
    print_response(res)
    assert res.status_code == 405


def test_category_id_todos_id_patch_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    any_id = '999'

    # When
    res = requests.patch(url + any_id + '/todos/' + any_id, headers=headers)

    # Then
    print_response(res)
    assert res.status_code == 405
