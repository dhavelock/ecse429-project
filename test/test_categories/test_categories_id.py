import pytest
import requests
import json
from test.common.helper import reset_system, create_category, print_response
import xml.dom.minidom

url = 'http://localhost:4567/categories/'


def setup_function(function):
    reset_system()


def teardown_function(function):
    pass


def test_get_category():

    # Given
    headers = {'Content-Type': 'application/json'}

    category1 = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category1_id = create_category(category1)['id']

    # When
    res = requests.get(url + category1_id, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['categories']) == 1
    assert res_body['categories'][0]['id'] == category1_id
    assert res_body['categories'][0]['title'] == category1['title']
    assert res_body['categories'][0]['description'] == category1['description']


def test_get_category_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    category1 = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category1_id = create_category(category1)['id']

    # When
    res = requests.get(url + category1_id, headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200


def test_get_category_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json'}

    # When
    res = requests.get(url + str(123), headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 404


def test_put_category_valid_body():

    # Given
    headers = {'Content-Type': 'application/json'}

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    edited_category = {
        'title': 'A different title',
        'description': 'a different description'
    }

    # When
    res = requests.put(url + category_id, headers=headers,
                       data=json.dumps(edited_category))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['id'] == category_id
    assert res_body['title'] == edited_category['title']
    assert res_body['description'] == edited_category['description']


def test_put_category_valid_body_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    edited_category = {
        'title': 'A different title',
        'description': 'a different description'
    }

    # When
    res = requests.put(url + category_id, headers=headers,
                       data=json.dumps(edited_category))

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

# Undocumented


def test_put_category_invalid_body():

    # Given
    headers = {'Content-Type': 'application/json'}

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    edited_category = {}

    # When
    res = requests.put(url + category_id, headers=headers,
                       data=json.dumps(edited_category))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 400
    assert res_body['errorMessages'][0] == 'title : field is mandatory'

# Undocumented


def test_put_category_invalid_attribute():

    # Given
    headers = {'Content-Type': 'application/json'}

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    edited_category = {
        'invalid attr': 'test'
    }

    # When
    res = requests.put(url + category_id, headers=headers,
                       data=json.dumps(edited_category))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 400
    assert res_body['errorMessages'][0] == 'Could not find field: invalid attr'


def test_put_category_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json'}

    invalid_id = '999'

    edited_category = {}

    # When
    res = requests.put(url + invalid_id, headers=headers,
                       data=json.dumps(edited_category))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Invalid GUID for ' + \
        invalid_id + ' entity category'


def test_post_category_valid_body():

    # Given
    headers = {'Content-Type': 'application/json'}

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    edited_category = {
        'title': 'A different title',
        'description': 'a different description'
    }

    # When
    res = requests.post(url + category_id, headers=headers,
                        data=json.dumps(edited_category))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['id'] == category_id
    assert res_body['title'] == edited_category['title']
    assert res_body['description'] == edited_category['description']


def test_post_category_valid_body_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    edited_category = {
        'title': 'A different title',
        'description': 'a different description'
    }

    # When
    res = requests.post(url + category_id, headers=headers,
                        data=json.dumps(edited_category))

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

# Undocumented


def test_post_category_partial_body():

    # Given
    headers = {'Content-Type': 'application/json'}

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    edited_category = {
        'description': 'new text here'
    }

    # When
    res = requests.post(url + category_id, headers=headers,
                        data=json.dumps(edited_category))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['id'] == category_id
    assert res_body['title'] == category['title']
    assert res_body['description'] == edited_category['description']

# Undocumented


def test_post_category_invalid_attribute():

    # Given
    headers = {'Content-Type': 'application/json'}

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    edited_category = {
        'invalid attr': 'test'
    }

    # When
    res = requests.put(url + category_id, headers=headers,
                       data=json.dumps(edited_category))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 400
    assert res_body['errorMessages'][0] == 'Could not find field: invalid attr'


def test_post_category_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json'}

    invalid_id = '999'

    edited_category = {}

    # When
    res = requests.post(url + invalid_id, headers=headers,
                        data=json.dumps(edited_category))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'No such category entity instance with GUID or ID ' + \
        invalid_id + ' found'


def test_delete_category():

    # Given
    headers = {'Content-Type': 'application/json'}

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    # When
    res = requests.delete(url + category_id, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200


def test_delete_category_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json'}

    invalid_id = '999'

    # When
    res = requests.delete(url + invalid_id, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find any instances with categories/' + invalid_id


def test_options_category_ok():

    # Given
    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    # When
    res = requests.options(
        url + category_id, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 200


def test_options_category_does_not_exist():

    # Given
    invalid_id = '999'

    # When
    res = requests.options(
        url + invalid_id, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 200


def test_head_category_ok():

    # Given
    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    # When
    res = requests.head(
        url + category_id, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 200


def test_head_category_does_not_exist():

    # Given
    invalid_id = '999'

    # When
    res = requests.head(
        url + invalid_id, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 404


def test_patch_category_not_allowed():

    # Given
    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    # When
    res = requests.patch(
        url + category_id, headers={'Content-Type': 'application/json'})

    # Then
    print_response(res)

    assert res.status_code == 405
