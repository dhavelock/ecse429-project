from behave import given, when, then, register_type, use_step_matcher
from test.common.helper import create_project

import parse

@parse.with_pattern(r"[a-zA-Z0-9_\s]+")
def parse_string(text):
    return text

register_type(str_value=parse_string)
use_step_matcher("cfparse")

@then('the response field "{field}" should be "{value:str_value?}"')
def step_impl(context, field, value):
    if value is None:
        value = ''

    assert context.response[field] == value

@then('the response should have the error message: "{error_message}"')
def step_impl(context, error_message):
    assert context.response['errorMessages'][0] == error_message