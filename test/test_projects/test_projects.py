import pytest
import requests
import json
from test.common.helper import reset_system, create_project, print_response

url = 'http://localhost:4567/projects'
headers = {'Content-Type': 'application/json' } 

def setup_function(function):
    reset_system()

def teardown_function(function):
    pass

def test_get_empty_response():

    # When
    res = requests.get(url, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['projects']) == 0

def test_get_non_empty_response():

    # Given
    project1 = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project2 = {
        'title': 'Project title 2',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim xyz'
    }

    create_project(project1)
    create_project(project2)

    # When
    res = requests.get(url, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['projects']) == 2

    # Get todos from list since there is no guarantee on ordering in the response
    res_project1 = [project for project in res_body['projects'] if project['title'] == project1['title']][0]
    res_project2 = [project for project in res_body['projects'] if project['title'] == project2['title']][0]

    assert res_project1['title'] == project1['title']
    assert res_project1['description'] == project1['description']
    assert res_project2['title'] == project2['title']
    assert res_project2['description'] == project2['description']

def test_project_put_not_allowed():

    # When
    res = requests.put(url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_post_project_valid_body():

    # Given
    project = {
        'title': 'Project title x',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim xyz'
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(project))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == project['title']
    assert res_body['description'] == project['description']

def test_post_project_invalid_body():
    
    # Given
    project = {
        'id': 1
    }

    # When
    res = requests.post(url, headers=headers, data=json.dumps(project))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 400

def test_delete_not_allowed():

    # When
    res = requests.delete(url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405

def test_options_ok():

    # When
    res = requests.options(url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_head_ok():

    # When
    res = requests.head(url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_patch_not_allowed():

    # When
    res = requests.patch(url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405