from test.common.helper import create_category, delete_category, update_category


def init_existing_categories(num=10):
    for i in range(num):
        title = 'Test Category ' + str(i+1)
        create_category({'title': title})

def add_some_categories(num=10):
    for i in range(num):
        title = 'Test Added Category ' + str(i + 1)
        create_category({'title': title})

def delete_some_categories(num=10):
    for i in range(num):
        delete_category(str(i+1))

def modify_some_categories(num=10):
    for i in range(num):
        category_id = str(i+1)
        data = {'description': 'Modified category with id ' + category_id}
        update_category(category_id, data)