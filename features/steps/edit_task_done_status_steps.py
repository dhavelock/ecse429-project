from behave import *
from test.common.helper import create_project, delete_project, get_projects, create_todo, create_todo_project_relation, get_todos, delete_todo, complete_todo, get_todo

@given('A todo task exists in the system with id "{id}"')
def step_impl(context, id):
    context.id = id

@given('the task has a incomplete done status')
def step_impl(context):
    context.todo = create_todo({'id': context.id, 'doneStatus': False})

@given('the task has a complete done status')
def step_impl(context):
    context.todo = create_todo({'id': context.id, 'doneStatus': True})

@given('the user requests to edit an invalid task id in the system')
def step_impl(context):
    context.id = '999'

@when('The user requests to complete the task')
def step_impl(context):
    complete_todo(context.id)

@then('The todo task with id "{id}" should be completed')
def step_impl(context, id):
    response = get_todo(context.id)
    assert len(response.json()) == 1

@then('The todo task with id "{id}" should not be completed with error message 404')
def step_impl(context, id):
    response = get_todo(context.id)
    assert response.status_code == 404