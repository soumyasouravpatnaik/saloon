import sqlite3
from utilities import find_by_user_phoneno, convert_to_string


def post(json_object=None, flag=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = flag
    # name, phone, email, password, joining_date, col = '', '', '', '', '', ''
    name = ''
    try:
        name = json_object.get('name'),
        phone = json_object.get('phone'),
        email = json_object.get('email'),
        password = json_object.get('password'),
        joining_date = json_object.get('joining_date')
        if flag in ['clients']:
            black_listed = json_object['black_listed']
            col = black_listed
            column = 'black_listed'
        if flag in ['stylists']:
            speciality = json_object['speciality']
            col = speciality
            column = 'speciality'
        check_user = find_by_user_phoneno(phone, table_name)
        if check_user[1] == 'Exception':
            return {'message': 'Caught Exception'}, 500
        elif check_user[0] is True:
            return {'message': 'User with phone number - {} already exists'.format(convert_to_string(phone))}, 409
        query = "INSERT INTO %s(name,phone,email,password,joining_date,%s) VALUES('%s',%d,'%s','%s','%s','%s')" % (table_name, column, convert_to_string(name),
                                                                     int(convert_to_string(phone)), convert_to_string(email),
                                                                     convert_to_string(password),
                                                                     convert_to_string(joining_date),
                                                                     col)
        print(query)
        cursor.execute(query)
        connection.commit()
        return {'message': '{} - {} created successfully'.format(flag, convert_to_string(name))}, 201
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def get(flag=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = flag
    clients_details = []
    stylists_details = []
    try:
        query = "SELECT * FROM %s" % table_name
        print(query)
        records = cursor.execute(query)
        if table_name == 'clients':
            for items in records:
                print(items)
                clients_details.append({'id': items[0], 'name': items[1], 'phone': items[2], 'email': items[3],
                                        'password': items[4], 'joining_date': items[5], 'active': items[6]})
        else:
            for items in records:
                stylists_details.append({'id': items[0], 'name': items[1], 'phone': items[2], 'email': items[3],
                                        'speciality': items[4], 'joining_date': items[5], 'password': items[6]})
        return clients_details if table_name == 'clients' else stylists_details
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def get_one(flag=None, user_id=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = flag
    clients_details = []
    stylists_details = []
    try:
        query = "SELECT * FROM %s WHERE id=%d" % (table_name, int(convert_to_string(user_id)))
        print(query)
        records = cursor.execute(query)
        if table_name == 'clients':
            for items in records:
                print(items)
                clients_details.append({'id': items[0], 'name': items[1], 'phone': items[2], 'email': items[3],
                                        'password': items[4], 'joining_date': items[5], 'active': items[6]})
        else:
            for items in records:
                stylists_details.append({'id': items[0], 'name': items[1], 'phone': items[2], 'email': items[3],
                                        'speciality': items[4], 'joining_date': items[5], 'password': items[6]})
        return clients_details if table_name == 'clients' else stylists_details
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def login(json_object=None, flag=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = flag
    try:
        phone = json_object.get('phone'),
        password = json_object.get('password')
        if phone and password:
            query = "SELECT name FROM %s WHERE phone=%s AND password='%s'" % (table_name, int(convert_to_string(phone)),
                                                                            convert_to_string(password))
            cursor.execute(query)
            record = cursor.fetchone()
            print(convert_to_string(record))
            if record:
                return {'message': 'User - %s successfully Logged in..'% record}, 200
            else:
                return {'message': 'Invalid Credentials. Try Again'}, 200
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()