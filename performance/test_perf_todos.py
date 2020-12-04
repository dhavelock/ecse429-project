import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, print_response, create_project, create_category
import xml.dom.minidom
from datetime import datetime
from performance.todos import init_existing_todos

url = 'http://localhost:4567/todos'

num_todos = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

@pytest.mark.parametrize("num", num_todos)
def test_add_todo(num):

    t_start = datetime.utcnow().timestamp()

    reset_system()

    init_existing_todos(num=num)

    headers = dict()
    headers = {'Content-Type': 'application/json'} 

    # Given
    headers = {'Content-Type': 'application/json' } 

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    t_start_call = datetime.utcnow().timestamp()

    # When
    res = requests.post(url, headers=headers, data=json.dumps(todo))

    t_end_call = datetime.utcnow().timestamp()

    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == todo['title']
    assert res_body['doneStatus'] == str(todo['doneStatus']).lower()
    assert res_body['description'] == todo['description']

    t_end = datetime.utcnow().timestamp()

    t1 = t_end - t_start
    t2 = t_end_call - t_start_call

    f = open("perf_logs/add_todo_performance_test.csv", "a")
    f.write(str(datetime.now().isoformat()) + ',' + str(num) + ',' + str(t1) + ',' + str(t2) + '\n')
    f.close()


@pytest.mark.parametrize("num", num_todos)
def test_delete_todo(num):
    t_start = datetime.utcnow().timestamp()

    reset_system()

    init_existing_todos(num=num)

    # Given
    headers = {'Content-Type': 'application/json' }

    todo = {
        'title': 'Task title 1',
        'doneStatus': False,
        'description': 'this is a description'
    }

    todo_id = create_todo(todo)['id']

    t_start_call = datetime.utcnow().timestamp()

    # When
    res = requests.delete(url + '/' + todo_id, headers=headers)

    t_end_call = datetime.utcnow().timestamp()

    # Then
    print_response(res)

    assert res.status_code == 200

    t_end = datetime.utcnow().timestamp()

    t1 = t_end - t_start
    t2 = t_end_call - t_start_call

    f = open("perf_logs/delete_todo_performance_test.csv", "a")
    f.write(str(datetime.now().isoformat()) + ',' + str(num) + ',' + str(t1) + ',' + str(t2) + '\n')
    f.close()

@pytest.mark.parametrize("num", num_todos)
def test_put_todo_valid_body(num):

    t_start = datetime.utcnow().timestamp()

    reset_system()

    init_existing_todos(num=num)

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

    t_start_call = datetime.utcnow().timestamp()

    # When
    res = requests.put(url + '/' + todo_id, headers=headers, data=json.dumps(edited_todo))

    t_end_call = datetime.utcnow().timestamp()

    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['id'] == todo_id
    assert res_body['title'] == edited_todo['title']
    assert res_body['doneStatus'] == str(edited_todo['doneStatus']).lower()
    assert res_body['description'] == edited_todo['description']

    t_end = datetime.utcnow().timestamp()

    t1 = t_end - t_start
    t2 = t_end_call - t_start_call

    f = open("perf_logs/modify_todo_performance_test.csv", "a")
    f.write(str(datetime.now().isoformat()) + ',' + str(num) + ',' + str(t1) + ',' + str(t2) + '\n')
    f.close()