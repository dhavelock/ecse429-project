from behave import *
from test.common.helper import create_project

@given('I am creating a to do list title "{listTitle}"')
def step_impl(context, listTitle):
    context.listTitle = listTitle

@given('I am creating a to do list without a title')
def step_impl(context):
    context.listTitle = ''

@given('I set the description to "{description}"')
def step_impl(context, description):
    context.description = description

@when('I send the request to create the todo list')
def step_impl(context):

    body = dict()

    if 'listTitle' in context:
        body['title'] = context.listTitle

    if 'description' in context:
        body['description'] = context.description

    context.response = create_project(body)

@then('the response should have created a todo id')
def step_impl(context):
    assert context.response['id'].isdigit()
