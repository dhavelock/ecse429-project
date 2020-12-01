import pytest
import requests
import json
from test.common.helper import reset_system, create_category, print_response, create_todo, create_project
import xml.dom.minidom

url = 'http://localhost:4567/categories'
base_url = 'http://localhost:4567/'

def setup_function(function):
    reset_system()
    headers = dict()
    headers = {'Content-Type': 'application/json'}




def test_get_empty_response_categories():

    # Given
    headers = {'Content-Type': 'application/json'}

    # When
    res = requests.get(url, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['categories']) == 0


def test_get_empty_response_xml_categories():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    # When
    res = requests.get(url, headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200


def test_get_non_empty_response_categories():

    # Given
    headers = {'Content-Type': 'application/json'}

    category1 = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category2 = {
        'title': 'Category title 2',
        'description': 'this is another description'
    }

    create_category(category1)
    create_category(category2)

    # When
    res = requests.get(url, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['categories']) == 2

    # Get categories from list since there is no guarantee on ordering in the response
    res_category1 = [category for category in res_body['categories']
                     if category['title'] == category1['title']][0]
    res_category2 = [category for category in res_body['categories']
                     if category['title'] == category2['title']][0]

    assert res_category1['title'] == category1['title']
    assert res_category1['description'] == category1['description']
    assert res_category2['title'] == category2['title']
    assert res_category2['description'] == category2['description']


def test_get_non_empty_response_xml_categories():

    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    # Given
    category1 = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category2 = {
        'title': 'Category title 2',
        'description': 'this is another description'
    }

    create_category(category1)
    create_category(category2)

    # When
    res = requests.get(url, headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200


def test_put_not_allowed_categories():

    # When
    res = requests.put(url, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 405


def test_post_category_valid_body():

    # Given
    headers = {'Content-Type': 'application/json'}

    category = {
        'title': 'Task title 1',
        'description': 'this is a description'
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(category))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == category['title']
    assert res_body['description'] == category['description']

def test_post_category_valid_body_with_todo_relation():

    # Given
    headers = {'Content-Type': 'application/json'}

    todo = {
        'title': 'todo title'
    }

    todo_id = create_todo(todo)['id']

    category = {
        'title': 'Task title 1',
        'description': 'this is a description',
        'todos': [
            {
                'id': todo_id
            }
        ]
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(category))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == category['title']
    assert res_body['description'] == category['description']
    assert res_body['todos'][0]['id'] == todo_id

    # Assert category was added to todo
    updated_todo = requests.get(base_url + 'todos/' + todo_id, headers=headers)
    updated_todo_body = updated_todo.json()

    print_response(updated_todo)
    assert updated_todo_body['todos'][0]['categories'][0]['id'] == res_body['id']

def test_post_category_valid_body_with_project_relation():

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
        'title': 'Task title 1',
        'description': 'this is a description',
        'projects': [
            {
                'id': project_id
            }
        ]
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(category))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == category['title']
    assert res_body['description'] == category['description']
    assert res_body['projects'][0]['id'] == project_id

   # Assert category was added to project
    updated_project = requests.get(base_url + 'projects/' + project_id, headers=headers)
    updated_project_body = updated_project.json()

    print_response(updated_project)
    assert updated_project_body['projects'][0]['categories'][0]['id'] == res_body['id']


def test_post_category_valid_body_xml_categories():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    category = {
        'title': 'Task title 1',
        'description': 'this is a description'
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(category))

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 201


def test_post_category_invalid_body():

    # Given
    headers = {'Content-Type': 'application/json'}

    category = {
        'description': 'this is a description'
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(category))

    # Then
    print_response(res)

    assert res.status_code == 400


def test_delete_not_allowed_categories():

    # When
    res = requests.delete(url, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 405


def test_options_ok_categories():

    # When
    res = requests.options(url, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 200


def test_head_ok_categories():

    # When
    res = requests.head(url, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 200


def test_patch_not_allowed_categories():

    # When
    res = requests.patch(url, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 405
