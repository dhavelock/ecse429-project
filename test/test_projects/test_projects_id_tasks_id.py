import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, create_project, create_category, print_response
import xml.dom.minidom

url = 'http://localhost:4567/projects/'
headers = {'Content-Type': 'application/json' }

def setup_function(function):
    reset_system()

def teardown_function(function):
    pass

def test_get_project_id_categories_id_not_allowed():

    headers = {'Content-Type': 'application/json' }

    category = {
        'title': 'category title',
        'description': 'description of category'
    }

    category_id = create_category(category)['id']

    project = {
        'title': 'Project title',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    category_to_add = {
        'ID': category_id
    }

    project_id = create_project(project)['id']

    # When
    res = requests.get(url + project_id + '/categories/' + category_id, headers=headers)
    print_response(res)
    # Then
    #THIS DOESNT FOLLOW THE DOCUMENTATION - A PROBLEM
    assert res.status_code == 404