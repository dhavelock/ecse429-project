import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, create_category, print_response
import xml.dom.minidom

url = 'http://localhost:4567/todos/'

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
    res = requests.get(url + todo_id + '/categories', headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['categories'][0]['id'] == category_id
    assert res_body['categories'][0]['title'] == category['title']
    assert res_body['categories'][0]['description'] == category['description']
