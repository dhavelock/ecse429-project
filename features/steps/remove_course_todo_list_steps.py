from behave import *
from test.common.helper import create_project, delete_project, get_projects, create_todo, create_todo_project_relation, get_todos

@given('I have an existing todo list with title "{listTitle}"')
def step_impl(context, listTitle):
    context.listTitle = listTitle
    context.project = create_project({'title': listTitle})

@given('A set of todo items')
def step_impl(context):
    context.todos = list()
    for todo in context.table:

        todo_dict = todo.as_dict()

        if 'doneStatus' in todo_dict:
            todo_dict['doneStatus'] = todo_dict['doneStatus'] == 'True'

        context.todos.append(todo_dict)

        todo_id = create_todo(todo_dict)['id']
        create_todo_project_relation(todo_id, context.project['id'])

@when('I send the request to remove the todo list')
def step_impl(context):
    response = delete_project(context.project['id'])
    try:
        context.response = response.json()
    except:
        context.response = None

@then('The todo list with title "{listTitle}" should not exist')
def step_impl(context, listTitle):
    response = get_projects({'title': listTitle})
    assert len(response.json()['projects']) == 0

@then('The todos should have no project relations')
def step_impl(context):
    for todo in context.todos:
        response = get_todos({'title': todo['title']})
        assert 'taskof' not in response.json()['todos'][0]