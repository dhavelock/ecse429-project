from behave import *

from test.common.helper import get_todos, update_todo, get_todo

use_step_matcher("re")


@step('the todo task with title "(?P<taskTitle>.+)" has the description "(?P<oldDescription>.+)"')
def step_impl(context, taskTitle, oldDescription):
    all_todos = get_todos().json()['todos']
    todo_id = [t['id'] for t in all_todos if t['title'] == taskTitle][0]
    context.todo_id = todo_id
    update_todo(todo_id, {'description': oldDescription})


@when('I update the description of the task "(?P<taskTitle>.+)" to "(?P<newDescription>.+)"')
def step_impl(context, taskTitle, newDescription):
    context.code = update_todo(context.todo_id, {'description': newDescription}).status_code


@then('task "(?P<taskTitle>.+)" now has the description "(?P<newDescription>.+)"')
def step_impl(context, taskTitle, newDescription):
    assert get_todo(context.todo_id).json()['todos'][0]['description'] == newDescription


@step('the todo task with title "(?P<taskTitle>.+)" has no description')
def step_impl(context, taskTitle):
    all_todos = get_todos().json()['todos']
    todo_id = [t['id'] for t in all_todos if t['title'] == taskTitle][0]
    context.todo_id = todo_id
    update_todo(todo_id, {'description': ""})


@when('I remove the description of the task "(?P<taskTitle>.+)"')
def step_impl(context, taskTitle):
    update_todo(context.todo_id, {'description': ""})