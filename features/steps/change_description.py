from behave import *

use_step_matcher("re")


@step('the todo task with title "(?P<taskTitle>.+)" has the description "(?P<oldDescription>.+)"')
def step_impl(context, taskTitle, oldDescription):
    """
    :type context: behave.runner.Context
    :type taskTitle: str
    :type oldDescription: str
    """
    raise NotImplementedError(
        u'STEP: And the todo task with title "<taskTitle>" has the description "<oldDescription>"')


@when('I update the description of the task "(?P<taskTitle>.+)" to "(?P<newDescription>.+)"')
def step_impl(context, taskTitle, newDescription):
    """
    :type context: behave.runner.Context
    :type taskTitle: str
    :type newDescription: str
    """
    raise NotImplementedError(u'STEP: When I update the description of the task "<taskTitle>" to "<newDescription>"')


@then('task "(?P<taskTitle>.+)" now has the description "(?P<newDescription>.+)"')
def step_impl(context, taskTitle, newDescription):
    """
    :type context: behave.runner.Context
    :type taskTitle: str
    :type newDescription: str
    """
    raise NotImplementedError(u'STEP: Then task "<taskTitle>" now has the description "<newDescription>"')


@step('the todo task with title "(?P<taskTitle>.+)" has no description')
def step_impl(context, taskTitle):
    """
    :type context: behave.runner.Context
    :type taskTitle: str
    """
    raise NotImplementedError(u'STEP: And the todo task with title "<taskTitle>" has no description')


@when('I remove the description of the task "(?P<taskTitle>.+)"')
def step_impl(context, taskTitle):
    """
    :type context: behave.runner.Context
    :type taskTitle: str
    """
    raise NotImplementedError(u'STEP: When I remove the description of the task "<taskTitle>"')