import sqlite3


def drop_tables(table_name=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    if table_name is None:
        table = [
            'bookings',
            'services',
            'clients',
            'stylists'
        ]
    else:
        table = [
            table_name
        ]

    for items in table:
        drop_query = "DROP table %s" % items
        cursor.execute(drop_query)
        print('{} - Dropped'.format(items))
    connection.commit()
    connection.close()


def create_tables():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = {
        'clients': 'CREATE TABLE IF NOT EXISTS clients(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, phone INTEGER, email text, password text, joining_date text, black_listed text)',
        'stylists': 'CREATE TABLE IF NOT EXISTS stylists(id INTEGER PRIMARY KEY AUTOINCREMENT,name text, phone INTEGER, email text ,speciality text,joining_date text, password text)',
        'services': 'CREATE TABLE IF NOT EXISTS services(id INTEGER PRIMARY KEY AUTOINCREMENT,name text, price real)',
        'bookings': 'CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY AUTOINCREMENT,date text, slotID text, stylistID INTEGER, servicesID INTEGER, status text, clientID INTEGER)'
    }
    for item in query:
        cursor.execute(query[item])
        print('{} - Created'.format(item))
    connection.commit()
    connection.close()


if __name__ == '__main__':
    drop_tables()
    create_tables()







