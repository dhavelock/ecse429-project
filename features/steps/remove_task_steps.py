from behave import *
from test.common.helper import create_project, delete_project, get_projects, create_todo, create_todo_project_relation, get_todos, delete_todo, get_project_todos, delete_project_todo, get_todo

@given('I have a todo list with title "{listTitle}"')
def step_impl(context, listTitle):
    context.listTitle = listTitle
    context.project = create_project({'title': listTitle})

@given('the todo list has a task with title "{taskTitle}"')
def step_impl(context, taskTitle):
    context.taskTitle = taskTitle
    context.todo = create_todo({'title': taskTitle})
    create_todo_project_relation(context.todo['id'], context.project['id'])

@given('the todo list does not have a task with title "{taskTitle}')
def step_impl(context, taskTitle):
    context.taskTitle = taskTitle
    context.todo = create_todo({'title': taskTitle})

@given('I want to delete the invalid task with "{taskTitle}" from the todo list')
def step_impl(context, taskTitle):
    context.project_id = context.project['id']
    context.todo_id = context.todo['id']

@when('I request to delete the task with "{taskTitle}" from the todo list')
def step_impl(context, taskTitle):
    delete_project_todo(context.project['id'], context.todo['id'])

@when('I request to delete the task with "{taskTitle}" from the system')
def step_impl(context, taskTitle):
    delete_todo(context.todo['id'])

@when('I request to delete the invalid task')
def step_impl(context):
    context.response = delete_project_todo(context.project_id, context.todo_id)

@then('The todo task with taskTitle "{taskTitle}" should not exist on the todo list')
def step_impl(context, taskTitle):
    context.response = get_project_todos(context.project['id'])
    assert len(context.response.json()['todos']) == 0

@then('the task will be deleted from the system')
def step_impl(context):
    response = get_todo(context.todo['id'])
    assert (response.status_code) == 404

@then('I should see an error message with 404 status code')
def step_impl(context):
    assert (context.response.status_code) == 404