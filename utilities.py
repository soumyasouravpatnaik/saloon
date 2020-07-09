import sqlite3
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from constants import EMAIL_TEMPLATE, sender_email, smtp_ssl, port, email_standard, phone_standard,\
    id_standard, pass_standard, name_standard, sname_standard, price_standard
import random


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


def find_by_user_id(id=None, table_name=None):
    existence = False, None
    id = convert_to_string(name=id)
    try:
        if id:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            query = "SELECT name FROM %s WHERE id=%d" % (table_name, int(id))
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


def sendmail(receiver=None, name=None, def_password=None):
    # sender_email = "mail@souravtests.online"
    receiver_email = receiver
    password = "Amazon_2020"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    html = EMAIL_TEMPLATE.format(name, def_password)

    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_ssl, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def temp_password():
    one_part = random.randint(66, 90)
    sec_part = random.randint(98, 122)
    thr_part = random.randint(999, 9999)
    for_part = random.randint(98, 122)
    password = ''
    for i in range(8):
        password = chr(one_part) + chr(sec_part) + str(thr_part) + chr(for_part)
    return password


def validator(name=None, service_name=None, email=None, phone=None, number=None, password=None, price=None):
    success_capturer = []
    if name:
        if re.match(name_standard, name):
            success_capturer.append('True')
        else:
            success_capturer.append('False')
    if phone:
        if re.match(phone_standard, phone):
            success_capturer.append('True')
        else:
            success_capturer.append('False')
    if email:
        if re.search(email_standard, email):
            success_capturer.append('True')
        else:
            success_capturer.append('False')
    if number:
        if re.match(id_standard, number):
            success_capturer.append('True')
        else:
            success_capturer.append('False')
    if password:
        if re.match(pass_standard, password):
            success_capturer.append('True')
        else:
            success_capturer.append('False')
    if service_name:
        if re.match(sname_standard, service_name):
            success_capturer.append('True')
        else:
            success_capturer.append('False')
    if price:
        if re.match(price_standard, price):
            success_capturer.append('True')
        else:
            success_capturer.append('False')

    return success_capturer


# if __name__ == '__main__':
    # print(validator(name='Slot01'))
#     temp_password()
#     sendmail('mailsourav123@gmail.com', name="IronDome", def_password="HGFbsgedhsdf")