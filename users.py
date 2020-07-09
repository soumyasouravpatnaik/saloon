import sqlite3
from utilities import find_by_user_phoneno, convert_to_string, sendmail, temp_password, find_by_user_id, validator


def post(json_object=None, flag=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = flag
    try:
        name = convert_to_string(json_object.get('name'))
        phone = convert_to_string(json_object.get('phone'))
        email = convert_to_string(json_object.get('email'))
        password = convert_to_string(json_object.get('password'))
        joining_date = convert_to_string(json_object.get('joining_date'))
        black_listed = convert_to_string(json_object['black_listed'])
        validate = validator(name=name, phone=phone, email=email, password=password)
        print(validate)
        if 'False' in validate:
            return {'message': 'Data Validation Failed'}, 400
        check_user = find_by_user_phoneno(phone, table_name)
        if check_user[1] == 'Exception':
            return {'message': 'Caught Exception'}, 500
        elif check_user[0] is True:
            return {'message': 'User with phone number - {} already exists'.format(convert_to_string(phone))}, 409
        if flag in ['stylists']:
            speciality = convert_to_string(json_object['speciality'])
            stylist_query = "INSERT INTO %s(name,phone,email,password,joining_date,black_listed,speciality) " \
                            "VALUES('%s',%d,'%s','%s','%s','%s','%s')" % (table_name, name, int(phone), email,
                                                                          password, joining_date, black_listed,
                                                                          speciality)
            print(stylist_query)
            cursor.execute(stylist_query)
        else:
            client_query = "INSERT INTO %s(name,phone,email,password,joining_date,black_listed) VALUES('%s',%d,'%s'," \
                           "'%s','%s','%s')" % (table_name, name, int(phone), email, password, joining_date,
                                                black_listed)
            print(client_query)
            cursor.execute(client_query)
        connection.commit()
        return {'message': '{} - {} created successfully'.format(flag, name)}, 201
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
        if table_name == 'clients':
            query = "SELECT id,name,phone,email,password,joining_date,black_listed FROM %s" % table_name
            print(query)
            records = cursor.execute(query)
            for items in records:
                print(items)
                clients_details.append({'id': items[0], 'name': items[1], 'phone': items[2], 'email': items[3],
                                        'password': items[4], 'joining_date': items[5], 'inactive': items[6]})
        else:
            query = "SELECT id,name,phone,email,speciality,joining_date,password,black_listed FROM %s" % table_name
            print(query)
            records = cursor.execute(query)
            for items in records:
                stylists_details.append({'id': items[0], 'name': items[1], 'phone': items[2], 'email': items[3],
                                        'speciality': items[4], 'joining_date': items[5], 'password': items[6],
                                         'inactive': items[7]})
        final_data = clients_details if table_name == 'clients' else stylists_details
        return (final_data, 200) if final_data else ({'message': '{} not registered'.format(table_name)}, 404)
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
        password = convert_to_string(json_object.get('password'))
        validate = validator(phone=convert_to_string(phone), password=password)
        print(validate)
        if 'False' in validate:
            return {'message': 'Data Validation Failed'}, 400
        query = "SELECT name,black_listed FROM %s WHERE phone=%d AND password='%s'" % (table_name, int(convert_to_string(phone)),
                                                                                       password)
        cursor.execute(query)
        record = cursor.fetchone()
        print(convert_to_string(record[0]))
        if record:
            if convert_to_string(record[1]) == 'N':
                return {'message': 'User - %s successfully Logged in..' % convert_to_string(record[0])}, 200
            else:
                return {'message': 'User - %s is marked inactive. Please contact Admin..' % convert_to_string(record[0])}, 200
        else:
            return {'message': 'Invalid Credentials. Try Again'}, 200
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def password_reset(json_object=None, id=id, flag=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = flag
    try:
        id = convert_to_string(id)
        email = convert_to_string(json_object.get('email')).lower()
        validate = validator(email=email, number=id)
        print(validate)
        if 'False' in validate:
            return {'message': 'Data Validation Failed'}, 400
        # password = json_object.get('password')
        if email:
            query = "SELECT email,black_listed,name FROM %s WHERE LOWER(email)='%s' AND id=%d" % (table_name, email,
                                                                                                  int(id))
            cursor.execute(query)
            record = cursor.fetchone()
            # print(convert_to_string(record[0]))
            if record:
                if convert_to_string(record[1]) == 'N':
                    print(sendmail(receiver=convert_to_string(record[0]), name=convert_to_string(record[2]),
                                   def_password=convert_to_string(temp_password())))
                    return {'message': 'Password Reset mail sent to %s' % convert_to_string(record[0])}, 200
                else:
                    return {'message': 'User - %s is marked inactive. Please contact Admin..' % convert_to_string(
                        record[2])}, 200
            else:
                return {'message': 'Invalid email/password. Try Again'}, 200
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def update_profile(json_object=None, flag=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = flag
    try:
        name = json_object.get('name'),
        phone = json_object.get('phone'),
        email = json_object.get('email'),
        id = json_object.get('id')
        validate = validator(name=name, phone=phone, email=email, number=id)
        print(validate)
        if 'False' in validate:
            return {'message': 'Data Validation Failed'}, 400
        check_user = find_by_user_id(id, table_name)
        if check_user[1] == 'Exception':
            return {'message': 'Caught Exception'}, 500
        elif check_user[0] is False:
            return {'message': 'User doesn\'t exist'}, 409
        elif check_user[0] is True:
            if flag in ['stylists']:
                speciality = json_object['speciality']
                stylist_query = "UPDATE %s SET name='%s', phone=%d, email='%s', speciality='%s' WHERE id=%d" \
                                % (table_name, convert_to_string(name), int(convert_to_string(phone)),
                                   convert_to_string(email), convert_to_string(speciality), int(convert_to_string(id)))
                print(stylist_query)
                cursor.execute(stylist_query)
            else:
                client_query = "UPDATE %s SET name='%s', phone=%d, email='%s' WHERE id=%d" \
                                % (table_name, convert_to_string(name), int(convert_to_string(phone)),
                                   convert_to_string(email), int(convert_to_string(id)))
                print(client_query)
                cursor.execute(client_query)
        connection.commit()
        return {'message': 'Profile successfully updated'}, 201
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()
