import pytest
import requests
import json
from test.common.helper import reset_system, create_project, print_response
import xml.dom.minidom

url = 'http://localhost:4567/projects/'
headers = {'Content-Type': 'application/json' } 

def setup_function(function):
    reset_system()


def test_valid_id_get_response():

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
    res = requests.get(specific_project_id_url, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert len(res_body['projects']) == 1

    # Get id from specific project response
    res_project = [project for project in res_body['projects'] if project['title'] == project['title']][0]
    assert res_project['id'] == res_specific_project['id']

def test_get_project_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project_id = create_project(project)['id']

    # When
    res = requests.get(url + project_id, headers=headers)

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

def test_invalid_id_get_response():

    # Given
    # Create new project, increase id by 1 to get an id that doesnt exist in the system
    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    res_specific_project = create_project(project)
    specific_non_existing_id = int(res_specific_project['id']) + 1
    specific_project_id_url = url + str(specific_non_existing_id)

    # When
    res = requests.get(specific_project_id_url, headers=headers)
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 404

def test_project_valid_id_put():

    # Given
    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project_change = {
      'title': 'Project changed title'
    }

    res_specific_project = create_project(project)
    specific_id = res_specific_project['id']

    specific_project_id_url = url + specific_id

    # When
    res = requests.put(specific_project_id_url, headers=headers, data=json.dumps(project_change))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['title'] == project_change['title']

def test_project_valid_id_put_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project_change = {
      'title': 'Project changed title'
    }
    
    res_specific_project = create_project(project)
    specific_id = res_specific_project['id']

    specific_project_id_url = url + specific_id
    # When
    res = requests.put(specific_project_id_url, headers=headers, data=json.dumps(project_change))

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

def test_project_invalid_id_put():

    # Given
    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    project_change = {
      'title': 'Project changed title'
    }

    res_specific_project = create_project(project)

    res_specific_project = create_project(project)
    specific_non_existing_id = int(res_specific_project['id']) + 1
    specific_project_id_url = url + str(specific_non_existing_id)

    # When
    res = requests.put(specific_project_id_url, headers=headers, data=json.dumps(project_change))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 404

def test_project_valid_id_post():

    # Given
    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
    }

    project_change = {
      'description': 'This is a description'
    }

    res_specific_project = create_project(project)
    specific_id = res_specific_project['id']

    specific_project_id_url = url + specific_id

    # When
    res = requests.post(specific_project_id_url, headers=headers, data=json.dumps(project_change))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['description'] == project_change['description']

def test_project_valid_id_post_xml():

    # Given
    headers = {'Content-Type': 'application/json', 'Accept': 'application/xml'}

    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
    }

    project_change = {
      'description': 'This is a description'
    }

    res_specific_project = create_project(project)
    specific_id = res_specific_project['id']

    specific_project_id_url = url + specific_id

    # When
    res = requests.post(specific_project_id_url, headers=headers, data=json.dumps(project_change))

    # Then
    res_xml = xml.dom.minidom.parseString(res.content)
    print(res_xml.toprettyxml())

    assert res.status_code == 200

def test_project_invalid_id_post():

    # Given
    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
    }

    project_change = {
      'description': 'This is a description'
    }

    res_specific_project = create_project(project)

    res_specific_project = create_project(project)
    specific_non_existing_id = int(res_specific_project['id']) + 1
    specific_project_id_url = url + str(specific_non_existing_id)

    # When
    res = requests.put(specific_project_id_url, headers=headers, data=json.dumps(project_change))
    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 404

def test_delete_valid_project():

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
    res = requests.delete(specific_project_id_url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_delete_invalid_project():

    # Given
    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    res_specific_project = create_project(project)
    specific_non_existing_id = int(res_specific_project['id']) + 1
    specific_project_id_url = url + str(specific_non_existing_id)

    # When
    res = requests.delete(specific_project_id_url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 404

def test_options_project():

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
    res = requests.options(specific_project_id_url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_head_valid_project():

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
    res = requests.head(specific_project_id_url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 200

def test_head_invalid_project():

    # Given
    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    res_specific_project = create_project(project)
    specific_non_existing_id = int(res_specific_project['id']) + 1
    specific_project_id_url = url + str(specific_non_existing_id)

    # When
    res = requests.head(specific_project_id_url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 404

def test_patch_not_allowed():

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
    res = requests.patch(specific_project_id_url, headers=headers)

    # Then
    print_response(res)

    assert res.status_code == 405