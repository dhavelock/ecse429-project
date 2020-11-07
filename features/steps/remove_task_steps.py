from behave import *
from test.common.helper import create_project, delete_project, get_projects, create_todo, create_todo_project_relation, get_todos, delete_todo

@given('A todo task exists with id "{id}"')
def step_impl(context, id):
    context.id = id
    context.todo = create_todo(context.id)

@given('the user wants to delete the task with an invalid id')
def step_impl(context):
    context.id = '999'

@when('The user requests to delete the task with "{id}"')
def step_impl(context, id):
    delete_todo(id)

@when('the user requests to delete the invalid task')
def step_impl(context):
    print(context.id)
    context.response = delete_todo(context.id)

@then('The todo task with id "{id}" should not exist with a response 200 status code')
def step_impl(context, id):
    response = get_todos({'id': id})
    assert len(response.json()['todos']) == 0
    assert response.status_code == 200

@then('the user should see an error message with 404 status code')
def step_impl(context):
    assert (context.response.status_code) == 404