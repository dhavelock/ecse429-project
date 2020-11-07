from behave import *
from test.common.helper import get_project_tasks, print_response

@when('I submit the query for incomplete todo items')
def step_impl(context):
    response = get_project_tasks(context.project['id'], {'doneStatus': 'false'})
    context.incomplete_tasks = response.json()['todos']

@then('Only todo items with doneStatus of false should be returned')
def step_impl(context):
    for task in context.incomplete_tasks:
        assert task['doneStatus'] == 'false'