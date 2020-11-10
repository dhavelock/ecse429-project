from behave import *
from test.common.helper import create_project, create_todo, create_todo_project_relation, get_categories, \
    create_todo_category_relation, get_todos, get_category_todos, delete_category


@given("the following tasks exist")
def step_impl(context):
    for todo in context.table:
        todo_table = todo.as_dict()

        todo_dict = {'title': todo_table['taskTitle']}
        if 'doneStatus' in todo_table:
            todo_dict['doneStatus'] = todo_table['doneStatus'] == 'True'
        if 'description' in todo_table:
            todo_dict['description'] = todo_table['description']

        todo_id = create_todo(todo_dict)['id']

        if 'priorityLevel' in todo_table:
            category_id = get_categories({'title': todo_table['priorityLevel']}).json()['categories'][0]['id']
            create_todo_category_relation(todo_id, category_id)
        if 'project' in todo_table:
            project_id = create_project({'title': todo_table['project']})['id']
            create_todo_project_relation(todo_id, project_id)




@when('I submit a query for "{priorityLevel}" priority level tasks with a done status of "{doneStatus}"')
def step_impl(context, priorityLevel, doneStatus):
    try:
        category_id = get_categories({'title': priorityLevel}).json()['categories'][0]['id']
    except IndexError:
        category_id = context.cat_id
    response = get_category_todos(str(category_id), {'doneStatus': doneStatus.lower()})
    context.response = response.json()['todos']
    context.code = response.status_code


@then('the following list "{tasks}" of task titles is returned')
def step_impl(context, tasks):
    tasks = [t.strip() for t in tasks.split(',')]
    assert len(context.response) == len(tasks)
    for res in context.response:
        assert res['title'] in tasks


@then("I receive an empty list")
def step_impl(context):
    assert len(context.response) == 0


@step('I receive a status code "{statusCode}"')
def step_impl(context, statusCode):
    assert context.code == int(statusCode)


@given('the priority category "{priorityLevel}" has been deleted')
def step_impl(context, priorityLevel):
    context.cat_id = get_categories({'title': priorityLevel}).json()['categories'][0]['id']
    delete_category(context.cat_id).status_code
