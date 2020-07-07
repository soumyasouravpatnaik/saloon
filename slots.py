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