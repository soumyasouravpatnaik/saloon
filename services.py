import sqlite3
from utilities import convert_to_string, find_services_by_name


def post(json_object=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = 'services'
    try:
        service_name = json_object.get('service_name')
        service_price = json_object.get('price')
        check_service = find_services_by_name(name=service_name)
        if check_service[1] == 'Exception':
            return {'message': 'Caught Exception'}, 500
        elif check_service[0] is True:
            return {'message': 'Service name - {} already exists'.format(convert_to_string(service_name))}, 409
        query = "INSERT INTO %s(name,price) VALUES('%s','%s')" % (table_name, convert_to_string(service_name),
                                                                  service_price)
        print(query)
        cursor.execute(query)
        connection.commit()
        return {'message': 'Service created successfully'}, 201
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def get():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = 'services'
    service_details = []
    try:
        query = "SELECT * FROM %s" % table_name
        print(query)
        records = cursor.execute(query)
        for items in records:
            service_details.append({'id': items[0], 'service_name': items[1], 'price': items[2]})
        return service_details, 200
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def get_one(id=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = 'services'
    service_details = []
    try:
        query = "SELECT name,price FROM %s WHERE id=%d" % (table_name, id)
        print(query)
        records = cursor.execute(query)
        for items in records:
            service_details.append({'service_name': items[0], 'price': items[1]})
        return service_details
    except Exception as e:
        print(str(e))
        # return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()