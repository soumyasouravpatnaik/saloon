from flask import Flask, jsonify, request, render_template
import bookings
import services
import users
import slots
import utilities
import db
app = Flask(__name__)
app.secret_key = 'ABC'


@app.before_first_request
def tables():
    db.create_tables()


client = [
    {
        'name': 'Bets',
        'phno': '1234567890',
        'email': 'abc@admin.com',
        'password': '123456'
    }
]
# Register Client


@app.route('/client', methods=['POST'])
def register_client():
    request_data = request.get_json()
    new_client = {
        'name': request_data['name'],
        'phone': request_data['phone'],
        'email': request_data['email'],
        'password': request_data['password'],
        'joining_date': request_data['joining_date'],
        'black_listed': request_data['black_listed']
    }
    response_object = users.post(json_object=new_client, flag='clients')
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/client/login', methods=['POST'])
def login_client():
    request_data = request.get_json()
    credentials = {
        'phone': request_data['phone'],
        'password': request_data['password'],

    }
    response_object = users.login(json_object=credentials, flag='clients')
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/clients', methods=['GET'])
def get_all_clients_details():
    response_object = users.get(flag='clients')
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/client/<int:id>', methods=['GET'])
def get_one_client_details(id):
    return jsonify(users.get_one(flag='clients', user_id=id)), 200


@app.route('/client/<int:id>', methods=['DELETE'])
def delete_client(id):
    pass


@app.route('/blacklist/client/<int:id>/<string:active>', methods=['PUT'])
def toggle_blacklist_client(id, active):
    response_object = utilities.toggle_black_list(user_id=id, flag='clients', active=active)
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/blacklist/stylist/<int:id>/<string:active>', methods=['PUT'])
def toggle_blacklist_stylist(id, active):
    response_object = utilities.toggle_black_list(user_id=id, flag='stylists', active=active)
    return jsonify(response_object[0]), int(response_object[1])

# Register Stylist


@app.route('/stylist', methods=['POST'])
def register_stylist():
    request_data = request.get_json()
    new_stylist = {
        'name': request_data['name'],
        'phone': request_data['phone'],
        'email': request_data['email'],
        'password': request_data['password'],
        'joining_date': request_data['joining_date'],
        'speciality': request_data['speciality'],
        'black_listed': request_data['black_listed'],
    }
    response_object = users.post(json_object=new_stylist, flag='stylists')
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/stylists', methods=['GET'])
def get_stylists():
    response_object = users.get(flag='stylists')
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/stylist/login', methods=['POST'])
def login_stylist():
    request_data = request.get_json()
    credentials = {
        'phone': request_data['phone'],
        'password': request_data['password'],

    }
    response_object = users.login(json_object=credentials, flag='stylists')
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/stylist/<int:id>', methods=['GET'])
def get_one_stylist_details(id):
    return jsonify(users.get_one(flag='stylists', user_id=id)), 200


@app.route('/client/<int:id>/changepwd', methods=['PUT'])
def change_client_password(id):
    request_data = request.get_json()
    credentials = {
        'email': request_data['email'],

    }
    response_object = users.password_reset(json_object=credentials, id=id, flag='clients')
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/stylist/<int:id>/changepwd', methods=['PUT'])
def change_stylist_password(id):
    request_data = request.get_json()
    credentials = {
        'email': request_data['email'],

    }
    response_object = users.password_reset(json_object=credentials, id=id, flag='stylists')
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/stylist/<int:id>/updateprofile', methods=['PUT'])
def stylist_changeprofile(id):
    request_data = request.get_json()
    update_stylist = {
        'name': request_data['name'],
        'phone': request_data['phone'],
        'email': request_data['email'],
        'speciality': request_data['speciality'],
        'id': id
    }
    response_object = users.update_profile(json_object=update_stylist, flag='stylists')
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/client/<int:id>/updateprofile', methods=['PUT'])
def client_changeprofile(id):
    request_data = request.get_json()
    update_client = {
        'name': request_data['name'],
        'phone': request_data['phone'],
        'email': request_data['email'],
        'id': id
    }
    response_object = users.update_profile(json_object=update_client, flag='clients')
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/booking', methods=['POST'])
def open_booking_call():
    request_data = request.get_json()
    booking = {
        'booking_date': request_data['booking_date'],
    }
    response_object = bookings.post(json_object=booking)
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/booking', methods=['PUT'])
def create_booking_call():
    request_data = request.get_json()
    booking = {
        'booking_date': request_data['booking_date'],
        'slotID': request_data['slotID'],
        'stylistID': request_data['stylistID'],
        'servicesID': request_data['servicesID'],
        'clientID': request_data['clientID']
    }
    response_object = bookings.put(json_object=booking)
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/booking', methods=['DELETE'])
def cancel_booking_call():
    request_data = request.get_json()
    booking = {
        'booking_id': request_data['booking_id'],
        'slot_id': request_data['slotID']
    }
    response_object = bookings.cancel(json_object=booking)
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/booking', methods=['GET'])
def get_booking():
    response_object = bookings.get()
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/services', methods=['POST'])
def create_services():
    request_data = request.get_json()
    new_services = {
        'service_name': request_data['service_name'],
        'price': request_data['price'],
    }
    response_object = services.post(json_object=new_services)
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/services', methods=['GET'])
def get_all_services():
    response_object = services.get()
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/appointments/<int:date>', methods=['GET'])
def get_all_appointments(date):
    print(date)
    response_object = bookings.get_appointments(date)
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/slots', methods=['GET'])
def get_slots():
    response_object = slots.get_all_slots()
    return jsonify(response_object[0]), int(response_object[1])


if __name__ == '__main__':
    app.run(debug=True, port=8000)