import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

slots = [
('Slot01','10:00 - 11:00'),
('Slot02','11:00 - 12:00'),
('Slot03','12:00 - 13:00'),
('Slot04','13:00 - 14:00'),
('Slot05','14:00 - 15:00'),
('Slot06','15:00 - 16:00'),
('Slot07','16:00 - 17:00'),
('Slot08','17:00 - 18:00'),
('Slot09','18:00 - 19:00'),
('Slot10','19:00 - 20:00'),
('Slot11','20:00 - 21:00'),
('Slot12','21:00 - 22:00')
]
# create_clients_table = "CREATE TABLE IF NOT EXISTS clients(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, phone INTEGER, " \
#                         "email text, password text, joining_date text, black_listed text)"
# create_stylists_table = "CREATE TABLE IF NOT EXISTS stylists(id INTEGER PRIMARY KEY AUTOINCREMENT,name text, phone INTEGER," \
#                         " email text ,speciality text,joining_date text, password text)"
# create_services_table = "CREATE TABLE IF NOT EXISTS services(id INTEGER PRIMARY KEY AUTOINCREMENT,name text, price real)"
# create_bookings_table = "CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY AUTOINCREMENT,date text, slotID text, " \
#                         "stylistID INTEGER, servicesID INTEGER, status text, clientID INTEGER)"
# create_slots_table = "CREATE TABLE IF NOT EXISTS slots(id INTEGER PRIMARY KEY AUTOINCREMENT,slotID text, slotDesc text)"
# create_test_table = "CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY AUTOINCREMENT,slotID text, slotDesc text)"

# cursor.execute(create_clients_table)
# cursor.execute(create_stylists_table)
# cursor.execute(create_services_table)
# cursor.execute(create_bookings_table)
# cursor.execute(create_slots_table)
# cursor.execute(create_test_table)
# stmt = "INSERT INTO slots (slotID, slotDesc) VALUES (?, ?)"
# cursor.executemany(stmt, slots)

# cursor.execute("DROP table bookings")
# cursor.execute("SELECT * FROM slots")
# record = cursor.fetchall()
# for row in record:
#     print(row)




connection.commit()
connection.close()
