import sqlite3


def find_by_user_phoneno(phone=None, table_name=None):
    existence = False, None
    phone = convert_to_string(name=phone)
    try:
        if phone:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            query = "SELECT name FROM %s WHERE phone=%d" % (table_name, int(phone))
            cursor.execute(query)
            record = cursor.fetchone()
            if record:
                existence = True, None
                # return {'message': 'User with phone number - {} already exists'.format(phone)}, 409
            cursor.close()
            connection.close()
            return existence
    except:
        existence = False, 'Exception'
        return existence


def find_booking_date(table_name='bookings', date=None):
    existence = False, None
    date = convert_to_string(name=date)
    # inner_record = None
    try:
        if date:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            query_check_date = "SELECT id FROM %s WHERE date='%s'" % (
                table_name, date)
            print(query_check_date)
            record = cursor.execute(query_check_date)
            outer_record = record.fetchone()
            if outer_record:
                existence = True, None
                # return {'message': 'User with phone number - {} already exists'.format(phone)}, 409
            cursor.close()
            connection.close()
            return existence
    except:
        existence = False, 'Exception'
        return existence


def find_slots_by_stylists(date=None, slot_id=None, stylist_id=None, table_name='bookings'):
    existence = False, None
    date = convert_to_string(name=date)
    slot_id = convert_to_string(name=slot_id)
    stylist_id = convert_to_string(name=stylist_id)
    try:
        if date:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            query = "SELECT id FROM %s WHERE date='%s' AND stylistID=%d AND slotID='%s' AND status='Open'" % (table_name, date,
                                                                                            int(stylist_id), slot_id)
            cursor.execute(query)
            record = cursor.fetchone()
            if record:
                existence = True, None
                # return {'message': 'User with phone number - {} already exists'.format(phone)}, 409
            cursor.close()
            connection.close()
            return existence
    except:
        existence = False, 'Exception'
        return existence


def check_blacklisted(stylist_id=None, table_name='stylists'):
    existence = False, None, table_name
    stylist_id = convert_to_string(name=stylist_id)
    try:
        if stylist_id:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            query = "SELECT id FROM %s WHERE id=%d AND black_listed='%s'" % (table_name, int(stylist_id), 'N')
            cursor.execute(query)
            record = cursor.fetchone()
            if record:
                existence = True, None, table_name
                # return {'message': 'User with phone number - {} already exists'.format(phone)}, 409
            cursor.close()
            connection.close()
            return existence
    except:
        existence = False, 'Exception', table_name
        return existence


def find_services_by_name(name=None):
    existence = False, None
    name = convert_to_string(name=name)
    table_name = 'services'
    try:
        if name:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            query = "SELECT id FROM %s WHERE name='%s'" % (table_name, name)
            cursor.execute(query)
            record = cursor.fetchone()
            if record:
                existence = True, None
                # return {'message': 'User with phone number - {} already exists'.format(phone)}, 409
            cursor.close()
            connection.close()
            return existence
    except:
        existence = False, 'Exception'
        return existence


def convert_to_string(name=None):
    if isinstance(name, tuple):
        print(name)
        name = str(name[0])
        print(type(name))
        return name
    return str(name)


def toggle_black_list(user_id=None, flag=None, active='N'):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "UPDATE %s SET black_listed='%s' WHERE id='%s'" % (flag, active, user_id)
        cursor.execute(query)
        connection.commit()
        connection.close()
        return {'message': 'BlackList - {} updated successfully for {} - {}'. format(active, flag, user_id)}, 201
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
