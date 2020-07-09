import sqlite3
from utilities import find_booking_date, find_slots_by_stylists, convert_to_string, check_blacklisted, validator
import users
import services
import slots
from constants import TABLES
table_name = TABLES[3]


def post(json_object=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    # table_name = 'bookings'
    try:
        booking_date = json_object.get('booking_date')
        validate = validator(number=convert_to_string(booking_date))
        print(validate)
        if 'False' in validate:
            return {'message': 'Data Validation Failed'}, 400
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
    # table_name = 'bookings'
    try:
        booking_date = json_object.get('booking_date')
        slotID = json_object.get('slotID'),
        stylistID = json_object.get('stylistID'),
        servicesID = json_object.get('servicesID'),
        clientID = json_object.get('clientID'),
        validate_stylistID = validator(number=convert_to_string(stylistID))
        validate_servicesID = validator(number=convert_to_string(servicesID))
        validate_clientID = validator(number=convert_to_string(clientID))
        validate_booking_date = validator(number=convert_to_string(booking_date))
        validate = validate_stylistID + validate_servicesID + validate_clientID + validate_booking_date
        if 'False' in validate:
            return {'message': 'Data Validation Failed'}, 400
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
            not_blacklisted_stylists = check_blacklisted(stylistID)
            not_blacklisted_clients = check_blacklisted(clientID, table_name=TABLES[0])

            if not_blacklisted_stylists[0] and not_blacklisted_clients[0]:
                query = "INSERT INTO %s(date, slotID,stylistID,servicesID,status,clientID) " \
                        "VALUES('%s', '%s', %d, %d, '%s', %d)" \
                % (table_name, convert_to_string(booking_date), convert_to_string(slotID),
                   int(convert_to_string(stylistID)),int(convert_to_string(servicesID)), 'Open',
                   int(convert_to_string(clientID)))
                print(query)
                cursor.execute(query)
                connection.commit()
                return {'message': 'Booking created for date - {} successfully'.format(
                    convert_to_string(booking_date))}, 201
            else:
                print(not_blacklisted_stylists)
                print(not_blacklisted_clients)

                return ({'message': 'Stylists is inactive.'}, 201) if not_blacklisted_stylists[0] is False else \
                    ({'message': 'Client is inactive.'}, 201)
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def get():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    booking_details = []
    try:
        query = "SELECT id, date, slotID, stylistID, servicesID, status, clientID FROM %s" % table_name
        print(query)
        records = cursor.execute(query)
        for items in records:
            booking_details.append({'id': items[0], 'booking_date': items[1], 'slotID': items[2], 'stylistID': items[3],
                                     'servicesID': items[4], 'status': items[5], 'clientID': items[6]})
        return booking_details, 200
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def cancel(json_object):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    # table_name = 'bookings'
    try:
        booking_id = json_object.get('booking_id')
        slot_id = convert_to_string(json_object.get('slot_id'))
        validate = validator(number=booking_id)
        print(validate)
        if 'False' in validate:
            return {'message': 'Data Validation Failed'}, 400
        query = "UPDATE %s SET status='Cancelled' WHERE id=%d AND slotID='%s'" % (table_name,
                                                                          int(convert_to_string(booking_id)), slot_id)
        print(query)
        cursor.execute(query)
        connection.commit()
        return {'message': 'Booking - {} cancelled successfully'.format(
            convert_to_string(booking_id))}, 201
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


def get_appointments(date):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    booking_details = []
    try:
        query = "SELECT stylistID, date, slotID, servicesID, status, clientID FROM %s WHERE date='%s'" % (table_name,
                                                                                              convert_to_string(date))
        print(query)
        records = cursor.execute(query)
        record = records.fetchall()
        for items in record:
            if items[4] != 'Cancelled' and items[4] is not None:
                stylist_name = convert_to_string(users.get_one('stylists', items[0])[0]['name'])
                client_name = convert_to_string(users.get_one('clients', items[5])[0]['name'])
                service_name = convert_to_string(services.get_one(items[3])[0]['service_name'])
                slot = convert_to_string(slots.get_one(items[2])[0]['slotDesc'])
                booking_details.append({'stylist_name': stylist_name, 'booking_date': items[1], 'slotID': slot,
                                        'services': service_name, 'status': items[4], 'client': client_name})
                print(booking_details)
        return (booking_details, 200) if bool(booking_details) else ({'message': 'No appointments available for {}'
                                                                     .format(date)}, 404)
    except Exception as e:
        print(str(e))
        return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()


