from behave import *
from test.common.helper import create_project, create_category, delete_project, get_projects, create_todo, create_todo_project_relation, get_todos, delete_todo, complete_todo, get_todo, create_todo_category_relation, get_project


@given('I have an existing to do list with title "{listTitle}"')
def step_impl(context, listTitle):
    context.listTitle = listTitle
    context.project = create_project({'title': listTitle})


@given('I have an existing task with title "{taskTitle}"')
def step_impl(context, taskTitle):
    context.taskTitle = taskTitle
    context.todo = create_todo({'title': taskTitle})


@when('I enter the task title "{taskTitle}"')
def step_impl(context, taskTitle):
    context.taskTitle = taskTitle


@when('I enter the task description "{taskDescription}"')
def step_impl(context, taskDescription):
    context.taskDescription = taskDescription


@when('I request to create the task')
def step_impl(context):

    body = dict()

    if 'taskTitle' in context:
        body['title'] = context.listTitle

    if 'taskDescription' in context:
        body['description'] = context.taskDescription

    context.todo = create_todo(body)


@when('I request to add the task to the to do list')
def step_impl(context):
    create_todo_project_relation(context.todo['id'], context.project['id'])


@when('I request to add an invalid task to the to do list')
def step_impl(context):
    create_todo_project_relation('999', context.project['id'])


@then('the to do list with title "{listTitle}" should include the task with title "{taskTitle}"')
def step_impl(context, listTitle, taskTitle):
    response = get_project(context.project['id'])
    assert response.json()[
        'projects'][0]['tasks'][0]['id'] == context.todo['id']


@then('the to do list with title "{listTitle}" should not include any tasks')
def step_impl(context, listTitle):
    response = get_project(context.project['id'])
    assert 'tasks' not in response.json()['projects'][0]
