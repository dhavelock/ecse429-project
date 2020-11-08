from behave import *
from test.common.helper import create_project, create_category, delete_project, get_projects, create_todo, create_todo_project_relation, get_todos, delete_todo, complete_todo, get_todo, create_todo_category_relation


@given('a todo task exists in the system with title "{todoTitle}"')
def step_impl(context, todoTitle):
    context.todo_id = create_todo({'title': todoTitle})['id']


@given('a HIGH priority category exists in the system')
def step_impl(context):
    context.category_id = create_category({'title': 'HIGH'})['id']


@given('a MEDIUM priority category exists in the system')
def step_impl(context):
    context.category_id = create_category({'title': 'MEDIUM'})['id']


@given('a LOW priority category exists in the system')
def step_impl(context):
    context.category_id = create_category({'title': 'LOW'})['id']


@given('a category exists in the system with title "{categoryTitle}"')
def step_impl(context, categoryTitle):
    context.category_id_1 = create_category({'title': categoryTitle})['id']


@given('a todo task exists with title "{todoTitle}" and category with title "{categoryTitle}"')
def step_impl(context, todoTitle, categoryTitle):
    context.todo_id = create_todo({'title': todoTitle})['id']
    create_todo_category_relation(
        context.todo_id, context.category_id_1)


@when('I categorize the task as HIGH priority')
def step_impl(context):
    create_todo_category_relation(context.todo_id, context.category_id)


@when('I categorize the task as MEDIUM priority')
def step_impl(context):
    create_todo_category_relation(context.todo_id, context.category_id)


@when('I categorize the task as LOW priority')
def step_impl(context):
    create_todo_category_relation(context.todo_id, context.category_id)


@when('I request to add a HIGH priority cartegorization to the task using an invalid id')
def step_impl(context):
    create_todo_category_relation(context.todo_id, '999')


@then('the todo task with title "{todoTitle}" should have the HIGH priority categorization')
def step_impl(context, todoTitle):
    response = get_todo(context.todo_id)
    assert response.json()[
        'todos'][0]['categories'][0]['id'] == context.category_id


@then('the todo task with title "{todoTitle}" should have the MEDIUM priority categorization')
def step_impl(context, todoTitle):
    response = get_todo(context.todo_id)
    assert response.json()[
        'todos'][0]['categories'][0]['id'] == context.category_id


@then('the todo task with title "{todoTitle}" should have the LOW priority categorization')
def step_impl(context, todoTitle):
    response = get_todo(context.todo_id)
    assert response.json()[
        'todos'][0]['categories'][0]['id'] == context.category_id


@then('the todo task ith title "{todoTitle}" should have both categories associated with it')
def step_impl(context, todoTitle):
    response = get_todo(context.todo_id)
    assert len(response.json()[
        'todos'][0]['categories']) == 2


@then('the todo task should not have any category relations')
def step_impl(context):
    response = get_todo(context.todo_id)
    assert 'categories' not in response.json()['todos'][0]
