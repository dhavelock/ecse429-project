from test.common.helper import create_todo, delete_todo, update_todo


def init_existing_todos(num=10):
    for i in range(num):
        title = 'Test Todo ' + str(i+1)
        create_todo({'title': title})

def add_some_todos(num=10):
    for i in range(num):
        title = 'Test Added Todo ' + str(i + 1)
        create_todo({'title': title})

def delete_some_todos(num=10):
    for i in range(num):
        delete_todo(str(i+1))

def modify_some_todos(num=10):
    for i in range(num):
        todo_id = str(i+1)
        data = {'description': 'Modified todo with id ' + todo_id}
        update_todo(todo_id, data)
