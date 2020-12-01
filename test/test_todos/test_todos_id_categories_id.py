import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, create_category, print_response, create_todo_category_relation
import xml.dom.minidom

base_url = 'http://localhost:4567/todos/'
category_url = 'http://localhost:4567/categories/'

def url(todo_id, category_id):
    return base_url + str(todo_id) + '/categories/' + str(category_id)

def setup_function(function):
    reset_system()


def test_get_todo_category_not_allowed():

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
    res = requests.get(url(todo_id, category_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_put_todo_category_not_allowed():

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
    res = requests.put(url(todo_id, category_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_post_todo_category_not_allowed():

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
    res = requests.post(url(todo_id, category_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_delete_todo_category():

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

    create_todo_category_relation(todo_id, category_id)

    # When
    res = requests.delete(url(todo_id, category_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

    # Fetch todo and category to assert that the catgeory relationship was deleted
    updated_todo = requests.get(base_url + todo_id, headers=headers)
    updated_todo_body = updated_todo.json()

    print('Todo:')
    print_response(updated_todo)

    assert updated_todo_body['todos'][0].get('categories') is None

    updated_category = requests.get(category_url + category_id, headers=headers)
    updated_category_body = updated_category.json()

    print('Category:')
    print_response(updated_category)

    assert updated_category_body['categories'][0].get('todos') is None

def test_delete_todo_category_relationship_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    category = {
        'title': 'category title',
        'description': 'description of category'
    }

    other_category = {
        'title': 'category title',
        'description': 'description of category'
    }

    category_id = create_category(category)['id']
    other_category_id = create_category(other_category)['id']

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
    res = requests.delete(url(todo_id, other_category_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 404

    # Fetch todo to assert that the catgeory relationship was not deleted
    updated_todo = requests.get(base_url + todo_id, headers=headers)
    updated_todo_body = updated_todo.json()

    print_response(updated_todo)

    assert updated_todo_body['todos'][0]['categories'][0]['id'] == category_id

def test_delete_todo_category_todo_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    category = {
        'title': 'category title',
        'description': 'description of category'
    }

    category_id = create_category(category)['id']

    todo = {
        'title': 'todo title'
    }

    todo_id = create_todo(todo)['id']

    create_todo_category_relation(todo_id, category_id)

    invalid_id = '999'

    # When
    res = requests.delete(url(invalid_id, category_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 400

def test_delete_todo_category_category_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    category_id = '999'

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    # When
    res = requests.delete(url(todo_id, category_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 404

def test_options_todos_category_ok():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.options(url(any_id, any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

# Undocumented / Unexcpected (should return 405)
def test_head_todos_category_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.head(url(any_id, any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 404

def test_patch_todos_category_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.patch(url(any_id, any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405