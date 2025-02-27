import subprocess
import requests
import time
import os
import glob

def start_server(server_output_file='todo_manager_log.txt'):

    with open(server_output_file, "w") as outfile:
        subprocess.Popen(['java', '-jar', 'runTodoManagerRestAPI-1.5.5.jar'], stdout=outfile)

    # Wait for server to start
    line = ''
    while line != b' e.g. http://localhost:4567\n':
        line = subprocess.check_output(['tail', '-1', server_output_file])

    # Confirm server has started up
    tries = 0
    while tries < 10:
        try:
            requests.get('http://localhost:4567')
            break
        except requests.exceptions.ConnectionError as e:
            print('Connecting to server...')
            time.sleep(0.5)

    if tries == 10:
        print('Failed to start up server')
        exit(1)

def shutdown_server():
    try:
        requests.get('http://localhost:4567/shutdown')
    except requests.exceptions.ConnectionError as e:
        print('\nTodo Manager Shutdown')

def pytest_sessionstart(session):
    files = glob.glob('./perf_logs/*')
    for f in files:
        os.remove(f)

    start_server()

def pytest_sessionfinish(session, exitstatus):
    shutdown_server()