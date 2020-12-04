import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, print_response, create_project, create_category
import xml.dom.minidom
from datetime import datetime
from performance.projects import init_existing_projects

url = 'http://localhost:4567/projects'

num_todos = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

@pytest.mark.parametrize("num", num_todos)
def test_add_project(num):

    t_start = datetime.utcnow().timestamp()

    reset_system()

    init_existing_projects(num=num)

    headers = {'Content-Type': 'application/json' } 

    # Given
    project = {
        'title': 'Project title x',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim xyz'
    }

    t_start_call = datetime.utcnow().timestamp()

    # When
    res = requests.post(url, headers=headers, data=json.dumps(project))

    t_end_call = datetime.utcnow().timestamp()

    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == project['title']
    assert res_body['description'] == project['description']

    t_end = datetime.utcnow().timestamp()

    t1 = t_end - t_start
    t2 = t_end_call - t_start_call

    f = open("perf_logs/add_project_performance_test.csv", "a")
    f.write(str(datetime.now().isoformat()) + ',' + str(num) + ',' + str(t1) + ',' + str(t2) + '\n')
    f.close()


@pytest.mark.parametrize("num", num_todos)
def test_delete_project(num):

    t_start = datetime.utcnow().timestamp()

    reset_system()

    init_existing_projects(num=num)

    headers = {'Content-Type': 'application/json' } 

    # Given
    project = {
        'title': 'Project title 1',
        'completed': False,
        'active': True,
        'description': 'agna aliqua. Ut enim abc'
    }

    res_specific_project = create_project(project)
    specific_id = res_specific_project['id']

    specific_project_id_url = url + '/' + specific_id

    t_start_call = datetime.utcnow().timestamp()

    # When
    res = requests.delete(specific_project_id_url, headers=headers)

    t_end_call = datetime.utcnow().timestamp()

    # Then
    print_response(res)

    assert res.status_code == 200

    t_end = datetime.utcnow().timestamp()

    t1 = t_end - t_start
    t2 = t_end_call - t_start_call

    f = open("perf_logs/delete_project_performance_test.csv", "a")
    f.write(str(datetime.now().isoformat()) + ',' + str(num) + ',' + str(t1) + ',' + str(t2) + '\n')
    f.close()


@pytest.mark.parametrize("num", num_todos)
def test_modify_project(num):

    t_start = datetime.utcnow().timestamp()

    reset_system()

    init_existing_projects(num=num)

    headers = {'Content-Type': 'application/json' } 

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

    specific_project_id_url = url + '/' + specific_id

    t_start_call = datetime.utcnow().timestamp()

    # When
    res = requests.put(specific_project_id_url, headers=headers, data=json.dumps(project_change))

    t_end_call = datetime.utcnow().timestamp()

    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['title'] == project_change['title']

    t_end = datetime.utcnow().timestamp()

    t1 = t_end - t_start
    t2 = t_end_call - t_start_call

    f = open("perf_logs/modify_project_performance_test.csv", "a")
    f.write(str(datetime.now().isoformat()) + ',' + str(num) + ',' + str(t1) + ',' + str(t2) + '\n')
    f.close()