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

def test_get_project_empty_categories():

    # Given
    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    res_specific_project = create_project(project)
    specific_id = res_specific_project['id']

    specific_project_id_url = url + specific_id

    # When
    res = requests.get(specific_project_id_url + '/categories', headers=headers)
    res_body = res.json()

    # Then
    print_response(res)
    assert res.status_code == 200
    assert len(res_body['categories']) == 0

def test_get_project_with_categories():

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

    # When
    res = requests.get('http://localhost:4567/projects/' + project_id, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)
    assert res.status_code == 200
    assert res_body['projects'][0]['categories'][0]['id'] == category_id
    assert len(res_body['projects'][0]['categories'][0]) == 1

def test_get_project_with_categories_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'} 

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

    # When
    res = requests.get(url + project_id + '/categories', headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

# Undocumented - found through exploratory testing
def test_post_invalid_project_with_categories():

    # Given
    headers = {'Content-Type': 'application/json' }

    category = {
        'title': 'category title',
        'description': 'description of category'
    }

    category_id = str(create_category(category)['id'])

    project = {
        'title': 'Project title',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    category_to_add = {
        'ID': int(category_id)
    }

    res_specific_project = create_project(project)
    specific_non_existing_id = int(res_specific_project['id']) + 1
    specific_project_id_url = url + str(specific_non_existing_id)

    # When
    res = requests.post(specific_project_id_url + '/categories', headers=headers, data=json.dumps(category_to_add) )
    res_body = res.json()

    # Then
    print_response(res)
    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find parent thing for relationship projects/' + str(specific_non_existing_id) + '/categories'

def test_post_project_with_invalid_categories():

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
        'description': 'agna aliqua. Ut enim abc'
    }

    category_to_add = {
        'ID': invalid_category_id
    }

    project_id = create_project(project)['id']

    # When
    res = requests.post(url + project_id + '/categories', headers=headers, data=json.dumps(category_to_add))
    res_body = res.json()

    # Then
    print_response(res)
    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find thing matching value for ID'

def test_project_id_category_put_not_allowed():

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
    res = requests.put(url + project_id + '/categories', headers=headers, data=json.dumps(category_to_add))

    # Then
    print_response(res)
    assert res.status_code == 405

def test_project_id_category_delete_not_allowed():

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
    res = requests.delete(url + project_id + '/categories', headers=headers, data=json.dumps(category_to_add))

    # Then
    print_response(res)
    assert res.status_code == 405

def test_project_id_category_options_OK():

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
    res = requests.options(url + project_id + '/categories', headers=headers, data=json.dumps(category_to_add))

    # Then
    print_response(res)
    assert res.status_code == 200

def test_project_id_category_head_OK():

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
    res = requests.head(url + project_id + '/categories', headers=headers, data=json.dumps(category_to_add))

    # Then
    print_response(res)
    assert res.status_code == 200

def test_project_id_category_patch_not_allowed():

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
    res = requests.patch(url + project_id + '/categories', headers=headers, data=json.dumps(category_to_add))

    # Then
    print_response(res)

    assert res.status_code == 405



