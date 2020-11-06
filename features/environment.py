from test.common.helper import reset_system
from conftest import start_server, shutdown_server

def before_all(context):
    start_server(server_output_file='behave_log.txt')

def before_scenario(context, scenario):
    reset_system()

def after_all(context):
    shutdown_server()