from behave import *
from test.common.helper import create_todo

@given('I am creating a to do list title "{listTitle}"')
def step_impl(context, listTitle):
    context.listTitle = listTitle

@given('I set the description to "{description}"')
def step_impl(context, description):
    context.description = description

@when('I send the request to create the todo list')
def step_impl(context):
    body = {
        "title": context.listTitle,
        "description": context.description
    }

    context.response = create_todo(body)

@then('the response should have title "{listTitle}" with description "{description}"')
def step_impl(context, listTitle, description):
    assert context.response['title'] == listTitle
    assert context.response['description'] == description
    assert context.response['doneStatus'] == "false"
    assert context.response['id'].isdigit()
