from behave import *
from test.common.helper import create_project, create_category, delete_project, get_projects, create_todo, create_todo_project_relation, get_todos, delete_todo, complete_todo, get_todo, create_todo_category_relation


@given('a todo task exists in the system with title "{todoTitle}"')
def step_impl(context, todoTitle):
    context.todo = create_todo({'title': todoTitle})


@given('a "{priorityLevel}" priority category exists in the system')
def step_impl(context, priorityLevel):
    context.category = create_category({'title': priorityLevel})


@given('a category exists in the system with title "{categoryTitle}"')
def step_impl(context, categoryTitle):
    context.category_1 = create_category({'title': categoryTitle})


@given('a todo task exists with title "{todoTitle}" and category with title "{categoryTitle}"')
def step_impl(context, todoTitle, categoryTitle):
    context.todo = create_todo({'title': todoTitle})
    create_todo_category_relation(
        context.todo['id'], context.category_1['id'])


@when('I categorize the task as "{priorityLevel}" priority')
def step_impl(context, priorityLevel):
    create_todo_category_relation(context.todo['id'], context.category['id'])


@when('I request to add a "{priorityLevel}" priority cartegorization to the task using an invalid id')
def step_impl(context, priorityLevel):
    create_todo_category_relation(context.todo['id'], '999')


@then('the todo task with title "{todoTitle}" should have the "{priorityLevel}" priority categorization')
def step_impl(context, todoTitle, priorityLevel):
    response = get_todo(context.todo['id'])
    assert response.json()[
        'todos'][0]['categories'][0]['id'] == context.category['id']


@then('the todo task with title "{todoTitle}" should have both categories associated with it')
def step_impl(context, todoTitle):
    response = get_todo(context.todo['id'])
    assert len(response.json()[
        'todos'][0]['categories']) == 2


@then('the todo task should not have any category relations')
def step_impl(context):
    response = get_todo(context.todo['id'])
    assert 'categories' not in response.json()['todos'][0]
