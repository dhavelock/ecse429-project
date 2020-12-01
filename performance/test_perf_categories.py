import pytest
import requests
import json
from test.common.helper import reset_system, create_todo, print_response, create_project, create_category
import xml.dom.minidom
from datetime import datetime
from performance.categories import init_existing_categories

url = 'http://localhost:4567/categories'

num_todos = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

@pytest.mark.parametrize("num", num_todos)
def test_add_category(num):

    t_start = datetime.utcnow().timestamp()

    reset_system()

    init_existing_categories(num=num)

    # Given
    headers = {'Content-Type': 'application/json'}

    category = {
        'title': 'Task title 1',
        'description': 'this is a description'
    }

    t_start_call = datetime.utcnow().timestamp()

    # When
    res = requests.post(url, headers=headers, data=json.dumps(category))

    t_end_call = datetime.utcnow().timestamp()

    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 201
    assert res_body['title'] == category['title']
    assert res_body['description'] == category['description']

    t_end = datetime.utcnow().timestamp()

    t1 = t_end - t_start
    t2 = t_end_call - t_start_call

    f = open("perf_logs/add_category_performance_test.csv", "a")
    f.write(str(num) + ',' + str(t1) + ',' + str(t2) + '\n')
    f.close()


@pytest.mark.parametrize("num", num_todos)
def test_delete_category(num):

    t_start = datetime.utcnow().timestamp()

    reset_system()

    init_existing_categories(num=num)

    # Given
    headers = {'Content-Type': 'application/json'}

    category = {
        'title': 'Category title 1',
        'description': 'this is a description'
    }

    category_id = create_category(category)['id']

    t_start_call = datetime.utcnow().timestamp()

    # When
    res = requests.delete(url + '/' + category_id, headers=headers)

    t_end_call = datetime.utcnow().timestamp()

    # Then
    print_response(res)

    assert res.status_code == 200

    t_end = datetime.utcnow().timestamp()

    t1 = t_end - t_start
    t2 = t_end_call - t_start_call

    f = open("perf_logs/delete_category_performance_test.csv", "a")
    f.write(str(num) + ',' + str(t1) + ',' + str(t2) + '\n')
    f.close()


@pytest.mark.parametrize("num", num_todos)
def test_modify_category(num):

    t_start = datetime.utcnow().timestamp()

    reset_system()

    init_existing_categories(num=num)

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

    t_start_call = datetime.utcnow().timestamp()

    # When
    res = requests.put(url + '/' + category_id, headers=headers,
                       data=json.dumps(edited_category))

    t_end_call = datetime.utcnow().timestamp()

    res_body = res.json()

    # Then
    print_response(res)

    assert res.status_code == 200
    assert res_body['id'] == category_id
    assert res_body['title'] == edited_category['title']
    assert res_body['description'] == edited_category['description']

    t_end = datetime.utcnow().timestamp()

    t1 = t_end - t_start
    t2 = t_end_call - t_start_call

    f = open("perf_logs/modify_category_performance_test.csv", "a")
    f.write(str(num) + ',' + str(t1) + ',' + str(t2) + '\n')
    f.close()