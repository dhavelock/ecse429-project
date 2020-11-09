from behave import *
from test.common.helper import get_project_tasks, print_response

@given('I do not have an existing todo list with id "{id}"')
def step_impl(context, id):
    context.project = {
        'title': 'this does not exist',
        'id': id
    }

@when('I submit the query for incomplete todo items')
def step_impl(context):
    response = get_project_tasks(context.project['id'], {'doneStatus': 'false'})
    try:
        context.incomplete_tasks = response.json()['todos']
    except:
        context.incomplete_tasks = None

@then('Only todo items with doneStatus of false should be returned')
def step_impl(context):
    for task in context.incomplete_tasks:
        assert task['doneStatus'] == 'false'