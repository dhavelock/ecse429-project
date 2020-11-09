from behave import *

use_step_matcher("re")


@given('a task exists with title "(?P<taskTitle>.+)" and a priority level "(?P<oldPriority>.+)"')
def step_impl(context, taskTitle, oldPriority):
    """
    :type context: behave.runner.Context
    :type taskTitle: str
    :type oldPriority: str
    """
    raise NotImplementedError(
        u'STEP: Given a task exists with title "<taskTitle>" and a priority level "<oldPriority>"')


@when('I adjust the task "(?P<taskTitle>.+)" from "(?P<oldPriority>.+)" priority to "(?P<newPriority>.+)" priority')
def step_impl(context, taskTitle, oldPriority, newPriority):
    """
    :type context: behave.runner.Context
    :type taskTitle: str
    :type oldPriority: str
    :type newPriority: str
    """
    raise NotImplementedError(
        u'STEP: When I adjust the task "<taskTitle>" from "<oldPriority>" priority to "<newPriority>" priority')


@step('the "(?P<oldPriority>.+)" priority category should no longer contain the task "(?P<taskTitle>.+)"')
def step_impl(context, oldPriority, taskTitle):
    """
    :type context: behave.runner.Context
    :type oldPriority: str
    :type taskTitle: str
    """
    raise NotImplementedError(
        u'STEP: And the "<oldPriority>" priority category should no longer contain the task "<taskTitle>"')


@given('a task with title "(?P<taskTitle>.+)" does not exist')
def step_impl(context, taskTitle):
    """
    :type context: behave.runner.Context
    :type taskTitle: str
    """
    raise NotImplementedError(u'STEP: Given a task with title "<taskTitle>" does not exist')