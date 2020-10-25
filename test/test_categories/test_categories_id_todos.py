import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, create_category, print_response
import xml.dom.minidom

url = 'http://localhost:4567/categories/'
headers = {'Content-Type': 'application/json'}


def setup_function(function):
    reset_system()


def teardown_function(function):
    pass


def test_get_category_empty_todos():

    # Given
    category = {
        'title': 'Category title 1',
        'description': 'a description'
    }

    category_id = create_category(category)['id']

    specific_category_id_url = url + category_id

    # When
    res = requests.get(specific_category_id_url + '/todos', headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['todos']) == 0


def test_get_category_with_todos():

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
    res = requests.get('http://localhost:4567/categories/' +
                       category_id, headers=headers)
    res_body = res.json()

    print_response(res)

    # Then
    assert res.status_code == 200
    assert res_body['categories'][0]['todos'][0]['id'] == todo_id
    assert len(res_body['categories'][0]['todos'][0]) == 1


def test_get_category_with_todos_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

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
    res = requests.get(url + category_id + '/todos', headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200


def test_put_category_id_todos_not_allowed():

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

    todo_to_add = {
        'ID': todo_id
    }

    category_id = create_category(category)['id']

    # When
    res = requests.put(url + category_id + '/todos',
                       headers=headers, data=json.dumps(todo_to_add))

    # Then
    assert res.status_code == 405


def test_post_category_id_todos():

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

    todo_to_add = {
        'ID': todo_id
    }

    category_id = create_category(category)['id']

    # When
    res = requests.post(url + category_id + '/todos',
                        headers=headers, data=json.dumps(todo_to_add))

    # Then
    assert res.status_code == 201

    # When
    res = requests.get('http://localhost:4567/categories/' +
                       category_id, headers=headers)
    res_body = res.json()

    # Then, assert a relationship was made
    print_response(res)
    assert res_body['categories'][0]['todos'][0]['id'] == todo_id
    assert len(res_body['categories'][0]['todos'][0]) == 1


def test_post_category_id_todos_invalid_category_id():

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

    todo_to_add = {
        'ID': todo_id
    }

    category_id = create_category(category)['id']
    invalid_category_id = int(category_id) + 1

    # When
    res = requests.post(url + str(invalid_category_id) +
                        '/todos', headers=headers, data=json.dumps(todo_to_add))
    res_body = res.json()

    # Then
    print_response(res)
    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find parent thing for relationship categories/' + \
        str(invalid_category_id) + '/todos'


def test_post_category_id_todos_invalid_todo_id():

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
        'description': 'a description'
    }

    todo_to_add = {
        'ID': str(invalid_todo_id)
    }

    category_id = create_category(category)['id']

    # When
    res = requests.post(url + category_id + '/todos',
                        headers=headers, data=json.dumps(todo_to_add))
    res_body = res.json()

    # Then
    print_response(res)
    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find thing matching value for ID'


def test_delete_category_id_todos():

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

    todo_to_add = {
        'ID': todo_id
    }

    category_id = create_category(category)['id']

    # When
    res = requests.delete(url + category_id + '/todos',
                          headers=headers, data=json.dumps(todo_to_add))

    # Then
    print_response(res)
    assert res.status_code == 405


def test_category_id_todos_options_OK():

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

    todo_to_add = {
        'ID': todo_id
    }

    category_id = create_category(category)['id']

    # When
    res = requests.options(url + category_id + '/todos',
                           headers=headers, data=json.dumps(todo_to_add))

    # Then
    print_response(res)
    assert res.status_code == 200


def test_category_id_todos_head_OK():

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

    todo_to_add = {
        'ID': todo_id
    }

    category_id = create_category(category)['id']

    # When
    res = requests.head(url + category_id + '/todos',
                        headers=headers, data=json.dumps(todo_to_add))

    # Then
    print_response(res)
    assert res.status_code == 200


def test_category_id_todos_patch_not_allowed():

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

    todo_to_add = {
        'ID': todo_id
    }

    category_id = create_category(category)['id']

    # When
    res = requests.patch(url + category_id + '/todos',
                         headers=headers, data=json.dumps(todo_to_add))

    # Then
    print_response(res)
    assert res.status_code == 405
