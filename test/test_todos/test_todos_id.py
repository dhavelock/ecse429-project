import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, print_response
import xml.dom.minidom

url = 'http://localhost:4567/todos/'

def setup_function(function):
    reset_system()


def test_get_todo():

    # Given
    headers = {'Content-Type': 'application/json' }

    todo1 = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo1_id = create_todo(todo1)['id']

    # When
    res = requests.get(url + todo1_id, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['todos']) == 1
    assert res_body['todos'][0]['id'] == todo1_id
    assert res_body['todos'][0]['title'] == todo1['title']
    assert res_body['todos'][0]['doneStatus'] == str(todo1['doneStatus']).lower()
    assert res_body['todos'][0]['description'] == todo1['description']

def test_get_todo_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    todo1 = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo1_id = create_todo(todo1)['id']

    # When
    res = requests.get(url + todo1_id, headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200
    
def test_get_todo_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    # When
    res = requests.get(url + str(123), headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 404

def test_put_todo_valid_body():

    # Given
    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    edited_todo = {
        'title': 'A different title',
        'doneStatus': True,
        'description': 'a different description'
    }

    # When
    res = requests.put(url + todo_id, headers=headers, data=json.dumps(edited_todo))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['id'] == todo_id
    assert res_body['title'] == edited_todo['title']
    assert res_body['doneStatus'] == str(edited_todo['doneStatus']).lower()
    assert res_body['description'] == edited_todo['description']

def test_put_todo_valid_body_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    edited_todo = {
        'title': 'A different title',
        'doneStatus': True,
        'description': 'a different description'
    }

    # When
    res = requests.put(url + todo_id, headers=headers, data=json.dumps(edited_todo))

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

# Undocumented
def test_put_todo_invalid_body():

    # Given
    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    edited_todo = {}

    # When
    res = requests.put(url + todo_id, headers=headers, data=json.dumps(edited_todo))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 400
    assert res_body['errorMessages'][0] == 'title : field is mandatory'

# Undocumented
def test_put_todo_invalid_attribute():

    # Given
    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    edited_todo = {
        'invalid attr': 'test'
    }

    # When
    res = requests.put(url + todo_id, headers=headers, data=json.dumps(edited_todo))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 400
    assert res_body['errorMessages'][0] == 'Could not find field: invalid attr'

def test_put_todo_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    invalid_id = '999'

    edited_todo = {}

    # When
    res = requests.put(url + invalid_id, headers=headers, data=json.dumps(edited_todo))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Invalid GUID for ' + invalid_id + ' entity todo'

def test_post_todo_id_valid_body():

    # Given
    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    edited_todo = {
        'title': 'A different title',
        'doneStatus': True,
        'description': 'a different description'
    }

    # When
    res = requests.post(url + todo_id, headers=headers, data=json.dumps(edited_todo))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['id'] == todo_id
    assert res_body['title'] == edited_todo['title']
    assert res_body['doneStatus'] == str(edited_todo['doneStatus']).lower()
    assert res_body['description'] == edited_todo['description']

def test_post_todo_id_valid_body_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    edited_todo = {
        'title': 'A different title',
        'doneStatus': True,
        'description': 'a different description'
    }

    # When
    res = requests.post(url + todo_id, headers=headers, data=json.dumps(edited_todo))

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

# Undocumented
def test_post_todo_partial_body():

    # Given
    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    edited_todo = {
        'description': 'new text here'
    }

    # When
    res = requests.post(url + todo_id, headers=headers, data=json.dumps(edited_todo))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['id'] == todo_id
    assert res_body['title'] == todo['title']
    assert res_body['doneStatus'] == str(todo['doneStatus']).lower()
    assert res_body['description'] == edited_todo['description']

# Undocumented
def test_post_todo_invalid_attribute():

    # Given
    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    edited_todo = {
        'invalid attr': 'test'
    }

    # When
    res = requests.put(url + todo_id, headers=headers, data=json.dumps(edited_todo))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 400
    assert res_body['errorMessages'][0] == 'Could not find field: invalid attr'

def test_post_todo_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    invalid_id = '999'

    edited_todo = {}

    # When
    res = requests.post(url + invalid_id, headers=headers, data=json.dumps(edited_todo))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'No such todo entity instance with GUID or ID ' + invalid_id + ' found'

def test_delete_todo():

    # Given
    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    # When
    res = requests.delete(url + todo_id, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_delete_todo_does_not_exist():

    # Given
    headers = {'Content-Type': 'application/json' }

    invalid_id = '999'

    # When
    res = requests.delete(url + invalid_id, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 404
    assert res_body['errorMessages'][0] == 'Could not find any instances with todos/' + invalid_id

def test_options_todo_ok():

    # Given
    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    # When
    res = requests.options(url + todo_id, headers={'Content-Type': 'application/json' } )

    # Then
    print_response(res)

    assert res.status_code == 200

def test_options_todo_does_not_exist():

    # Given
    invalid_id = '999'

    # When
    res = requests.options(url + invalid_id, headers={'Content-Type': 'application/json' } )

    # Then
    print_response(res)

    assert res.status_code == 200

def test_head_todo_ok():

    # Given
    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    # When
    res = requests.head(url + todo_id, headers={'Content-Type': 'application/json' } )

    # Then
    print_response(res)

    assert res.status_code == 200

def test_head_todo_does_not_exist():

    # Given
    invalid_id = '999'

    # When
    res = requests.head(url + invalid_id, headers={'Content-Type': 'application/json' } )

    # Then
    print_response(res)

    assert res.status_code == 404


def test_patch_todo_not_allowed():

    # Given
    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    # When
    res = requests.patch(url + todo_id, headers={'Content-Type': 'application/json' } )

    # Then
    print_response(res)

    assert res.status_code == 405