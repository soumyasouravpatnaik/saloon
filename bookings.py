import sqlite3
from utilities import find_booking_date, find_slots_by_stylists, convert_to_string
import users
import services
from flask import jsonify


def post(json_object=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = 'bookings'
    try:
        booking_date = json_object.get('booking_date')
        check_existing_booking = find_booking_date(date=booking_date)
        if check_existing_booking[1] == 'Exception':
            return {'message': 'Caught Exception'}, 500
        elif check_existing_booking[0] is True:
            return {'message': 'Booking ID with date - {} already exists'.format(booking_date)}, 409
        query = "INSERT INTO %s(date) VALUES('%s')" % (table_name, booking_date)
        print(query)
        cursor.execute(query)
        connection.commit()
        return {'message': 'Booking opened for {} successfully'.format(convert_to_string(booking_date))}, 201
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def put(json_object=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = 'bookings'
    try:
        booking_date = json_object.get('booking_date')
        slotID = json_object.get('slotID'),
        stylistID = json_object.get('stylistID'),
        servicesID = json_object.get('servicesID'),
        clientID = json_object.get('clientID'),
        check_existing_booking = find_booking_date(date=booking_date)
        if check_existing_booking[1] == 'Exception':
            return {'message': 'Caught Exception'}, 500
        elif check_existing_booking[0] is False:
            return {'message': 'Booking not opened for date - {}. Contact Admin'.format(booking_date)}, 409
        check_slot_for_stylist = find_slots_by_stylists(date=booking_date, slot_id=slotID, stylist_id=stylistID)
        if check_slot_for_stylist[1] == 'Exception':
            return {'message': 'Caught Exception while verifying existing slot booking'}, 500
        elif check_slot_for_stylist[0] is True:
            return {'message': 'Already a booking exists for the same slot and same date. Please try another slot'
                .format(booking_date)}, 409
        elif check_slot_for_stylist[0] is False:
            query = "INSERT INTO %s(date, slotID,stylistID,servicesID,status,clientID) VALUES('%s', '%s', %d, %d, '%s', %d)" \
            %(table_name, convert_to_string(booking_date), convert_to_string(slotID), int(convert_to_string(stylistID)),int(convert_to_string(servicesID)), 'Open', int(convert_to_string(clientID)))
            print(query)
            cursor.execute(query)
            connection.commit()
            return {'message': 'Booking created for date - {} successfully'.format(
                convert_to_string(booking_date))}, 201
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def get():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = 'bookings'
    booking_details = []
    try:
        query = "SELECT id, date, slotID, stylistID, servicesID, status, clientID FROM %s" % table_name
        print(query)
        records = cursor.execute(query)
        for items in records:
            booking_details.append({'id': items[0], 'booking_date': items[1], 'slotID': items[2], 'stylistID': items[3],
                                     'servicesID': items[4], 'status': items[5], 'clientID': items[6]})
        return booking_details
    except Exception as e:
        print(str(e))
        return booking_details
    finally:
        cursor.close()
        connection.close()


def get_appointments(date):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = 'bookings'
    booking_details = []
    try:
        query = "SELECT stylistID, date, slotID, servicesID, status, clientID FROM %s WHERE date='%s'" % (table_name, convert_to_string(date))
        print(query)
        records = cursor.execute(query)
        record = records.fetchall()
        for items in record:
            if items[4] is not None:
                stylist_name = convert_to_string(users.get_one('stylists', items[0])[0]['name'])
                client_name = convert_to_string(users.get_one('clients', items[5])[0]['name'])
                service_name = convert_to_string(services.get_one(items[3])[0]['service_name'])
                booking_details.append({'stylist_name': stylist_name, 'booking_date': items[1], 'slotID': items[2],
                                        'services': service_name, 'status': items[4], 'client': client_name})
                print(booking_details)
        return booking_details
    except Exception as e:
        print(str(e))
    finally:
        cursor.close()
        connection.close()


