from behave import *
from test.common.helper import create_project, delete_project, get_projects, create_todo, create_todo_project_relation, get_todos, delete_todo, complete_todo, get_todo, edit_todo_done_status

@given('a todo list exists in the system with title "{listTitle}"')
def step_impl(context, listTitle):
    context.listTitle = listTitle
    context.project = create_project({'title': listTitle})
    context.project_id = context.project['id']

@given('the list has a task with the title "{taskTitle}" and a False done status')
def step_impl(context, taskTitle):
    context.taskTitle = taskTitle
    context.todo = create_todo({'title': taskTitle})
    create_todo_project_relation(context.todo['id'], context.project['id'])

@given('the list has a task with the title "{taskTitle}" and a True done status')
def step_impl(context, taskTitle):
    context.taskTitle = taskTitle
    context.todo = create_todo({'title': taskTitle, 'doneStatus' : True})
    create_todo_project_relation(context.todo['id'], context.project['id'])

@given('the todo list does not have an associated task with title "{taskTitle}')
def step_impl(context, taskTitle):
    context.taskTitle = taskTitle
    context.todo = create_todo({'title': taskTitle})

@when('I request to complete the task')
def step_impl(context):
    complete_todo(context.todo['id'])

@when('I request to complete the task with an invalid done status of "{invalidDoneStatus}"')
def step_impl(context, invalidDoneStatus):
    context.response = edit_todo_done_status(context.todo['id'], invalidDoneStatus)    

@then('The todo task with should be completed')
def step_impl(context):
    response = get_todo(context.todo['id'])
    print(response)
    assert response.json()[
        'todos'][0]['doneStatus'] == "true"

@then('I receive a status code of 400')
def step_impl(context):
    assert context.response.status_code == 400

@then('the done status of the todo task with "{taskTitle}" will not be changed')
def step_impl(context, taskTitle):
    response = get_todo(context.todo['id'])
    assert response.json()[
        'todos'][0]['doneStatus'] == "false"

