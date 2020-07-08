import sqlite3


def get_all_slots():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = 'slots'
    slots = []
    try:
        query = "SELECT id, slotID, slotDesc FROM %s" % table_name
        print(query)
        records = cursor.execute(query)
        for items in records:
            slots.append({'id': items[0], 'slotID': items[1], 'slotDesc': items[2]})
        return slots
    except Exception as e:
        print(str(e))
        return slots
    finally:
        cursor.close()
        connection.close()


def get_one(slot_id=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    table_name = 'slots'
    slot_details = []
    try:
        query = "SELECT slotDesc FROM %s WHERE slotID='%s'" % (table_name, slot_id)
        print(query)
        records = cursor.execute(query)
        for items in records:
            slot_details.append({'slotDesc': items[0]})
        return slot_details
    except Exception as e:
        print(str(e))
        # return {'message': 'Something went wrong'}, 500
    finally:
        cursor.close()
        connection.close()