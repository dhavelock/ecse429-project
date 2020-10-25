import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, create_category, print_response
import xml.dom.minidom

base_url = 'http://localhost:4567/todos/'

def url(id):
    return base_url + str(id) + '/categories'

def setup_function(function):
    reset_system()

def teardown_function(function):
    pass

def test_get_todos_categories():

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

    todo_id = create_todo(todo)['id']

    # When
    res = requests.get(url(todo_id), headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['categories'][0]['id'] == category_id
    assert res_body['categories'][0]['title'] == category['title']
    assert res_body['categories'][0]['description'] == category['description']

def test_get_todos_categories_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'} 

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

    todo_id = create_todo(todo)['id']

    # When
    res = requests.get(url(todo_id), headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

def test_get_todos_categories_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    invalid_id = 999

    # When
    res = requests.get(url(invalid_id), headers=headers)
    res_body = res.json()

    # Then
    print_response(res)
    
    assert len(res_body['todos']) == 0
    assert res.status_code == 200

def test_put_todos_categories_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    todo_id = 999

    # When
    res = requests.put(url(todo_id), headers=headers)

    # Then
    print_response(res)
    
    assert res.status_code == 405

def test_post_todos_categories():

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
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    body = {
        'id': category_id
    }

    # When
    res = requests.post(url(todo_id), headers=headers, data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 201

    # Fetch todo to assert that the catgeory relationship was created
    updated_todo = requests.get(base_url + todo_id, headers=headers)
    updated_todo_body = updated_todo.json()

    assert updated_todo_body['todos'][0]['categories'][0]['id'] == category_id

def test_post_todos_categories_invalid_body():

    # Given
    headers = {'Content-Type': 'application/json' }

    category_id = '999'

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    body = {
        'idd': category_id
    }

    # When
    res = requests.post(url(todo_id), headers=headers, data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 400

def test_post_todos_categories_todo_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    category = {
        'title': 'category title',
        'description': 'description of category'
    }

    category_id = create_category(category)['id']

    invalid_id = '999'

    body = {
        'id': category_id
    }

    # When
    res = requests.post(url(invalid_id), headers=headers, data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 404

def test_post_todos_categories_category_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    invalid_id = '999'

    body = {
        'id': invalid_id
    }

    # When
    res = requests.post(url(todo_id), headers=headers, data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 404

def test_delete_todos_categories_not_allowed():

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

    todo_id = create_todo(todo)['id']

    # When
    res = requests.delete(url(todo_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_options_todos_categories_ok():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.options(url(any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_head_todos_categories_ok():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.head(url(any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_delete_todos_categories_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    todo_id = '999'

    # When
    res = requests.put(url(todo_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405