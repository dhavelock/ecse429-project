import pytest
import requests
import json
from test.common.helper import reset_system, create_category, create_project, print_response, create_category_project_relation
import xml.dom.minidom

base_url = 'http://localhost:4567/categories/'
project_url = 'http://localhost:4567/projects/'


def url(category_id, project_id):
    return base_url + str(category_id) + '/projects/' + str(project_id)


def setup_function(function):
    reset_system()


def teardown_function(function):
    pass


def test_get_category_project_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    project = {
        'title': 'Office Work',
        'completed': False,
        'active': False,
        'description': 'a description'
    }

    project_id = create_project(project)['id']

    category = {
        'title': 'Category title 1',
        'description': 'this is a description',
        'projects': [
            {
                'id': project_id
            }
        ]
    }

    category_id = create_category(category)['id']

    # When
    res = requests.get(url(category_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405


def test_put_category_project_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    project = {
        'title': 'Office Work',
        'completed': False,
        'active': False,
        'description': 'a description'
    }

    project_id = create_project(project)['id']

    category = {
        'title': 'Category title 1',
        'description': 'this is a description',
        'projects': [
            {
                'id': project_id
            }
        ]
    }

    category_id = create_category(category)['id']

    # When
    res = requests.put(url(category_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405


def test_post_category_project_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    project = {
        'title': 'Office Work',
        'completed': False,
        'active': False,
        'description': 'a description'
    }

    project_id = create_project(project)['id']

    category = {
        'title': 'Category title 1',
        'description': 'this is a description',
        'projects': [
            {
                'id': project_id
            }
        ]
    }

    category_id = create_category(category)['id']

    # When
    res = requests.post(url(category_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405


def test_delete_category_project():

    # Given
    headers = {'Content-Type': 'application/json'}

    project = {
        'title': 'Office Work',
        'completed': False,
        'active': False,
        'description': 'a description'
    }

    project_id = create_project(project)['id']

    category = {
        'title': 'Category title 1',
        'description': 'this is a description',
        'projects': [
            {
                'id': project_id
            }
        ]
    }

    category_id = create_category(category)['id']

    create_category_project_relation(category_id, project_id)

    # When
    res = requests.delete(url(category_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

    # Fetch category and project to assert that the project relationship was deleted
    updated_category = requests.get(base_url + category_id, headers=headers)
    updated_category_body = updated_category.json()

    print('Category:')
    print_response(updated_category)

    assert updated_category_body['categories'][0].get('projects') is None

    updated_project = requests.get(project_url + category_id, headers=headers)
    updated_project_body = updated_project.json()

    print('Project:')
    print_response(updated_project)

    assert updated_project_body['projects'][0].get('categories') is None


def test_delete_category_project_relationship_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json'}

    project = {
        'title': 'Office Work',
        'completed': False,
        'active': False,
        'description': 'a description'
    }

    project_id = create_project(project)['id']

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    # When
    res = requests.delete(url(category_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 404


def test_delete_category_project_project_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json'}

    project_id = '999'

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    # When
    res = requests.delete(url(category_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 404


def test_delete_category_project_category_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json'}

    project = {
        'title': 'Office Work',
        'completed': False,
        'active': False,
        'description': 'a description'
    }

    project_id = create_project(project)['id']

    category = {
        'title': 'todo title'
    }

    category_id = create_category(category)['id']

    create_category_project_relation(category_id, project_id)

    invalid_id = '999'

    # When
    res = requests.delete(url(invalid_id, project_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 400


def test_options_category_project_ok():

    # Given
    headers = {'Content-Type': 'application/json'}

    any_id = '999'

    # When
    res = requests.options(url(any_id, any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200


def test_head_category_project_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    any_id = '999'

    # When
    res = requests.head(url(any_id, any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405


def test_patch_category_project_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    any_id = '999'

    # When
    res = requests.patch(url(any_id, any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405
