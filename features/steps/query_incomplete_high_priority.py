from behave import *
from test.common.helper import create_project, create_todo, create_todo_project_relation, get_categories, \
    create_todo_category_relation, get_todos


@given("the following tasks exist")
def step_impl(context):
    for todo in context.table:
        todo_table = todo.as_dict()

        todo_dict = {'title': todo_table['taskTitle']}
        if 'doneStatus' in todo_table:
            todo_dict['doneStatus'] = todo_table['doneStatus'] == 'True'
        if 'description' in todo_table:
            todo_dict['description'] = todo_table['description']

        context.category_id = get_categories({'title': todo_table['priorityLevel']}).json()['categories'][0]['id']
        project_id = create_project({'title': todo_table['project']})['id']
        todo_id = create_todo(todo_dict)['id']
        create_todo_project_relation(todo_id, project_id)
        create_todo_category_relation(todo_id, context.category_id)


@when('I submit a query for "{priorityLevel}" priority level tasks with a done status of "{doneStatus}"')
def step_impl(context, priorityLevel, doneStatus):
    context.response = get_todos({'doneStatus': doneStatus.lower(), 'category': {'id': context.category_id}}).json()['todos']


@then('the following list "{tasks}" of task titles is returned')
def step_impl(context, tasks):
    tasks = [t.strip() for t in tasks.split(',')]
    assert len(context.response) == len(tasks)
    for res in context.response:
        assert res['title'] in tasks


@then("I receive an empty list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then I receive an empty list')


@step('I receive a status code "{statusCode}"')
def step_impl(context, statusCode):
    """
    :type context: behave.runner.Context
    :type statusCode: str
    """
    raise NotImplementedError(u'STEP: And I receive a status code "<statusCode>"')


@given('the priority category "{priorityLevel}" has been deleted')
def step_impl(context, priorityLevel):
    """
    :type context: behave.runner.Context
    :type priorityLevel: str
    """
    raise NotImplementedError(u'STEP: Given the priority category "<priorityLevel>" has been deleted')