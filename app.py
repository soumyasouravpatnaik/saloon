from flask import Flask, jsonify, request, render_template
import bookings
import services
import users
import slots
app = Flask(__name__)

client = [
    {
        'name': 'Bets',
        'phno': '1234567890',
        'email': 'abc@admin.com',
        'password': '123456'
    }
]
# Register Client


@app.route('/client', methods=['POST', 'PUT'])
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


@app.route('/clientlogin', methods=['POST'])
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
    return jsonify(users.get(flag='clients')), 200


@app.route('/client/<int:id>', methods=['GET'])
def get_one_client_details(id):
    return jsonify(users.get_one(flag='clients', user_id=id)), 200


@app.route('/client/<int:id>', methods=['DELETE'])
def delete_client(id):
    pass


@app.route('/blacklistclient/<int:id>', methods=['PUT'])
def toggle_blacklist_client(id):
    pass

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
        'speciality': request_data['speciality']
    }
    response_object = users.post(json_object=new_stylist, flag='stylists')
    return jsonify(response_object[0]), int(response_object[1])


@app.route('/stylists', methods=['GET'])
def get_stylists():
    return jsonify(users.get(flag='stylists')), 200


@app.route('/stylistlogin', methods=['POST'])
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


def delete_stylists():
    pass
def stylist_engagement_plan():
    pass
def register_manager():
    pass

def get_manager():
    pass
def make_client_member():
    pass


# Slots
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


@app.route('/booking', methods=['GET'])
def get_booking():
    return jsonify(bookings.get()), 200


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
    return jsonify(services.get()), 200


@app.route('/appointments/<int:date>', methods=['GET'])
def get_all_appointments(date):
    print(date)
    data = bookings.get_appointments(date)
    if not data:
        return jsonify({'message': 'No appointments available for {}'.format(date)}), 404
    return jsonify(data), 200


@app.route('/slots', methods=['GET'])
def get_slots():
    return jsonify(slots.get_all_slots()), 200


if __name__ == '__main__':
    app.run(debug=True, port=8000)