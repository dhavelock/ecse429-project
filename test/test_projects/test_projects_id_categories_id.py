import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, create_project, create_category, print_response, create_category_project_relation
import xml.dom.minidom

url = 'http://localhost:4567/projects/'
headers = {'Content-Type': 'application/json' }

def setup_function(function):
    reset_system()

def teardown_function(function):
    pass

def test_get_project_id_categories_id_not_allowed():

    # Given
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
    
    # Then
    print_response(res)
    assert res.status_code == 405

def test_put_project_id_categories_id_not_allowed():

    # Given
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

    project_id = create_project(project)['id']

    # When
    res = requests.put(url + project_id + '/categories/' + category_id, headers=headers)
    
    # Then
    print_response(res)
    assert res.status_code == 405

def test_post_project_id_categories_id_not_allowed():

    # Given
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

    project_id = create_project(project)['id']

    # When
    res = requests.post(url + project_id + '/categories/' + category_id, headers=headers)

    # Then
    print_response(res)
    assert res.status_code == 405

def test_delete_project_id_categories_id_allowed():

    # Given
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
        'description': 'agna aliqua. Ut enim abc',
        'categories': [
            {
                'id': category_id
            }
        ]
    }

    project_id = create_project(project)['id']

    create_category_project_relation(category_id, project_id)

    # When
    res = requests.delete(url + project_id + '/categories/' + category_id, headers=headers)

    # Then
    assert res.status_code == 200

    # Check that relationship was deleted from both project and category
    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()

    print_response(res)
    assert res_body['projects'][0].get('categories') is None

    res = requests.get('http://localhost:4567/categories/' + category_id, headers=headers)
    res_body = res.json()

    print_response(res)
    assert res_body['categories'][0].get('projects') is None

def test_delete_project_id_categories_id_invalid_project():

    # Given
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
        'description': 'agna aliqua. Ut enim abc',
        'categories': [
            {
                'id': category_id
            }
        ]
    }

    project_id = create_project(project)['id']
    invalid_project_id = int(project_id) + 1

    # When
    res = requests.delete(url + str(invalid_project_id) + '/categories/' + category_id, headers=headers)

    # Then
    assert res.status_code == 400

    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()

    print_response(res)
    # assert relationship wasn't deleted
    assert len(res_body['projects'][0]) == 6
    assert res_body['projects'][0]['categories'][0]['id'] == category_id

def test_delete_project_id_categories_id_invalid_category():

    # Given
    headers = {'Content-Type': 'application/json' }

    category = {
        'title': 'category title',
        'description': 'description of category'
    }

    category_id = create_category(category)['id']
    invalid_category_id = int(category_id) + 1

    project = {
        'title': 'Project title',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc',
        'categories': [
            {
                'id': category_id
            }
        ]
    }

    category_to_add = {
        'ID': category_id
    }

    project_id = create_project(project)['id']

    # When
    res = requests.delete(url + project_id + '/categories/' + str(invalid_category_id), headers=headers)
    res_body = res.json()

    # Then
    print_response(res)
    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find any instances with projects/' + project_id + '/categories/' + str(invalid_category_id)

    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()
    
    print_response(res)
    # assert relationship wasn't deleted
    assert len(res_body['projects'][0]) == 6
    assert res_body['projects'][0]['categories'][0]['id'] == category_id

def test_delete_project_id_categories_id_no_relationship():

    # Given
    headers = {'Content-Type': 'application/json' }

    category1 = {
        'title': 'category title1',
        'description': 'description of category'
    }

    category2 = {
        'title': 'category title2',
        'description': 'description of category'
    }

    category_id1 = create_category(category1)['id']
    category_id2 = create_category(category2)['id']


    project = {
        'title': 'Project title',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc',
        'categories': [
            {
                'id': category_id1
            }
        ]
    }

    project_id = create_project(project)['id']

    # When
    res = requests.delete(url + project_id + '/categories/' + category_id2, headers=headers)
    res_body = res.json()

    # Then
    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find any instances with projects/' + project_id + '/categories/' + category_id2

    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()

    print_response(res)
    # assert relationship wasn't deleted
    assert len(res_body['projects'][0]) == 6
    assert res_body['projects'][0]['categories'][0]['id'] == category_id1

def test_project_id_categories_id_options_OK():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id ='999'

    # When
    res = requests.options(url + any_id + '/categories/' + any_id, headers=headers)

    # Then
    print_response(res)
    assert res.status_code == 200

def test_project_id_categories_id_head_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.head(url + any_id + '/categories/' + any_id, headers=headers)

    # Then
    print_response(res)
    assert res.status_code == 405

def test_project_id_categories_id_patch_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json' }

    any_id = '999'

    # When
    res = requests.patch(url + any_id + '/categories/' + any_id, headers=headers)

    # Then
    print_response(res)
    assert res.status_code == 405