import pytest
import requests
import json
from test.common.helper import reset_system, create_category, create_project, print_response
import xml.dom.minidom

base_url = 'http://localhost:4567/categories/'


def url(id):
    return base_url + str(id) + '/projects'


def setup_function(function):
    reset_system()


def teardown_function(function):
    pass


def test_get_categories_projects():

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
    res = requests.get(url(category_id), headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['projects'][0]['id'] == project_id
    assert res_body['projects'][0]['title'] == project['title']
    # assert res_body['projects'][0]['completed'] == project['completed']
    # assert res_body['projects'][0]['active'] == project['active']
    assert res_body['projects'][0]['description'] == project['description']
    assert res_body['projects'][0]['categories'][0]['id'] == category_id


def test_get_categories_projects_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

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
    res = requests.get(url(category_id), headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200


def test_get_categories_projects_category_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json'}

    invalid_id = '999'

    # When
    res = requests.get(url(invalid_id), headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['categories']) == 0


def test_put_categories_projects_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    any_id = '999'

    # When
    res = requests.put(url(any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405


def test_post_categories_projects():

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

    body = {
        'id': project_id
    }

    # When
    res = requests.post(url(category_id), headers=headers,
                        data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 201

    # Fetch category to assert relationship was created
    updated_category = requests.get(base_url + category_id, headers=headers)
    updated_category_body = updated_category.json()

    assert updated_category_body['categories'][0]['projects'][0]['id'] == project_id


def test_post_categories_projects_invalid_body():

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

    body = {
        'idd': project_id
    }

    # When
    res = requests.post(url(category_id), headers=headers,
                        data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 400

# Undocumented


def test_post_categories_projects_category_project_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json'}

    invalid_id = '999'

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    body = {
        'id': invalid_id
    }

    # When
    res = requests.post(url(category_id), headers=headers,
                        data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 404

# Undocumented


def test_post_categories_projects_category_category_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json'}

    invalid_id = '999'

    body = {
        'id': invalid_id
    }

    # When
    res = requests.post(url(invalid_id), headers=headers,
                        data=json.dumps(body))

    # Then
    print_response(res)

    assert res.status_code == 404


def test_delete_categories_projects_not_allowed():

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
    res = requests.delete(url(category_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405


def test_options_categories_projects_ok():

    # Given
    headers = {'Content-Type': 'application/json'}

    any_id = '999'

    # When
    res = requests.options(url(any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200


def test_head_categories_projects_ok():

    # Given
    headers = {'Content-Type': 'application/json'}

    any_id = '999'

    # When
    res = requests.head(url(any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200


def test_patch_categories_projects_not_allowed():

    # Given
    headers = {'Content-Type': 'application/json'}

    any_id = '999'

    # When
    res = requests.patch(url(any_id), headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405
