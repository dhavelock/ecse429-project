from test.common.helper import create_project, delete_project, update_project


def init_existing_projects(num=10):
    for i in range(num):
        title = 'Test Project ' + str(i+1)
        create_project({'title': title})

def add_some_projects(num=10):
    for i in range(num):
        title = 'Test Added Project ' + str(i + 1)
        create_project({'title': title})

def delete_some_projects(num=10):
    for i in range(num):
        delete_project(str(i+1))

def modify_some_projects(num=10):
    for i in range(num):
        project_id = str(i+1)
        data = {'description': 'Modified project with id ' + project_id}
        update_project(project_id, data)
