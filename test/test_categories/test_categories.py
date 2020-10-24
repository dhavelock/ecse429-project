import pytest
import requests
import json
from test.common.helper import reset_system, create_category, print_response
import xml.dom.minidom

url = 'http://localhost:4567/categories'


def setup_function(function):
    reset_system()
    headers = dict()
    headers = {'Content-Type': 'application/json'}


def teardown_function(function):
    pass


def test_get_empty_response():

    # Given
    headers = {'Content-Type': 'application/json'}

    # When
    res = requests.get(url, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['categories']) == 0


def test_get_empty_response_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    # When
    res = requests.get(url, headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200


def test_get_non_empty_response():

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


def test_get_non_empty_response_xml():

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


def test_put_not_allowed():

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


def test_post_category_valid_body_xml():

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


def test_delete_not_allowed():

    # When
    res = requests.delete(url, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 405


def test_options_ok():

    # When
    res = requests.options(url, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 200


def test_head_ok():

    # When
    res = requests.head(url, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 200


def test_patch_not_allowed():

    # When
    res = requests.patch(url, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 405
