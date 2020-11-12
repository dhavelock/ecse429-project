from behave import *

from test.common.helper import create_todo, get_categories, create_todo_category_relation, get_todo, \
    delete_todo_category_link, get_category_todos, get_todos, delete_todo

use_step_matcher("re")


@given('a task exists with title "(?P<taskTitle>.+)" and a priority level "(?P<oldPriority>.+)"')
def step_impl(context, taskTitle, oldPriority):
    context.todo_id = create_todo({'title': taskTitle})['id']
    category_id = get_categories({'title': oldPriority}).json()['categories'][0]['id']
    create_todo_category_relation(context.todo_id, category_id)


@when('I adjust the task "(?P<taskTitle>.+)" from "(?P<oldPriority>.+)" priority to "(?P<newPriority>.+)" priority')
def step_impl(context, taskTitle, oldPriority, newPriority):
    category_id = get_categories({'title': newPriority}).json()['categories'][0]['id']
    old_id = get_categories({'title': oldPriority}).json()['categories'][0]['id']
    context.code = delete_todo_category_link(context.todo_id, old_id).status_code
    create_todo_category_relation(context.todo_id, category_id)


@step('the "(?P<oldPriority>.+)" priority category should not contain the task "(?P<taskTitle>.+)"')
def step_impl(context, oldPriority, taskTitle):
    old_id = get_categories({'title': oldPriority}).json()['categories'][0]['id']
    response = get_category_todos(old_id).json()['todos']
    assert taskTitle not in [t['title'] for t in response]


@given('a task with title "(?P<taskTitle>.+)" does not exist')
def step_impl(context, taskTitle):
    task_del_id = create_todo({'title': taskTitle})['id']
    context.todo_id = task_del_id
    all_todos = get_todos().json()['todos']
    if taskTitle in [t['title'] for t in all_todos]:
        task_del = [t for t in all_todos if t['title'] == taskTitle]
        for t in task_del:
            delete_todo(t['id'])


@then('the task with title "(?P<taskTitle>.+)" should have the "(?P<priority>.+)" priority category')
def step_impl(context, taskTitle, priority):
    category_id = get_categories({'title': priority}).json()['categories'][0]['id']
    response = get_category_todos(category_id).json()['todos']
    assert taskTitle in [t['title'] for t in response]