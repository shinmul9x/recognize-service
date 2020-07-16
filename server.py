from flask import Flask, request
from flask_jsonpify import jsonify
from jwt import encode
from mqttmanager import subscribe_topics as subscribe_topics_mqtt
import apimanager
import dbmanager
from jwtdecoder import decode_token
from recognizedevice import train_model, recognize_device

app = Flask(__name__)
train_model()


@app.route('/', methods=['GET'])
def api_root():
    return 'Service Recognize electric device in house'


@app.route('/auth', methods=['GET'])
def api_get_token():
    token = request.args.get('token')
    if (token is not None) and (len(token) > 0):
        dbmanager.insert_info_user(token)
        topics = decode_token(token, 'topic')
        topics_mqtt = []
        for topic in topics:
            topics_mqtt.append(topic.get('topic'))
        subscribe_topics_mqtt(token, topics_mqtt)
    return jsonify('success')


@app.route('/recognize', methods=['POST'])
def api_recognize():
    if request.headers['Content-Type'] == 'application/json':
        characteristic = request.get_json()['amplitude']
        device_name = recognize_device(characteristic)
        # option = {
        #     'device_name': device_name,
        #     'token_id': None,
        #     'device_id': None,
        #     'authenticity': None,
        #     'amplitude': characteristic,
        #     'frequency': None
        # }
        # dbmanager.insert_characteristic(**option)
        return jsonify({'label': device_name})
    else:
        return '415 Unsupported Media Type'


@app.route('/api/login', methods=['POST'])
def api_login():
    headers = request.headers['Content-Type']
    if headers == 'application/x-www-form-urlencoded':
        username = request.form.get('username')
        if dbmanager.check_user(username):
            token = encode({'username': username}, '').decode('utf-8')
            return jsonify({'success': True, 'token': token})
        else:
            return jsonify({'message': 'miss user'}), 400
    elif headers == 'application/json':
        username = request.get_json()['username']
        if dbmanager.check_user(username):
            token = encode({'username': username}, '').decode('utf-8')
            return jsonify({'success': True, 'token': token})
        else:
            return jsonify({'message': 'miss user'}), 400
    else:
        return jsonify({'message': '415 Unsupported Media Type'}), 415


@app.route('/api/get-user-info', methods=['GET'])
def api_get_user_info():
    token = request.headers['x-access-token']
    username = decode_token(token, 'username')
    if username is None:  # can not decode token
        return jsonify({'message': 'miss token'}), 401
    # get info home, room from db
    info = dbmanager.get_user_info(username)
    if len(info) > 0:
        return jsonify({'success': True, 'homes': info}), 200
    else:  # no home link to this user
        return jsonify({'message': 'no home'}), 400


@app.route('/api/get-home', methods=['GET'])
def api_get_home():
    token = request.headers['x-access-token']
    username = decode_token(token, 'username')
    if username is None:
        return jsonify({'message': 'miss token'}), 401
    home = dbmanager.get_home(username)
    if len(home) > 0:
        return jsonify({'success': True, 'home': home}), 200
    else:
        return jsonify({'message': 'no home'}), 400


@app.route('/api/get-room/home/<home_id>', methods=['GET'])
def api_get_room(home_id):
    token = request.headers['x-access-token']
    username = decode_token(token, 'username')
    if username is None:
        return jsonify({'message': 'miss token'}), 400
    if dbmanager.check_user(username):
        room = dbmanager.get_room(username, home_id)
        if room is None:
            return jsonify({'message': 'home not exist'})
        elif len(room) > 0:
            return jsonify({'success': True, 'room': room}), 200
        else:
            return jsonify({'message': 'no room'}), 400
    return jsonify({'message': 'user does not exist'}), 400


@app.route('/api/get-device-list/room/<room_id>', methods=['GET'])
def api_get_device_list(room_id):
    token = request.headers['x-access-token']
    username = decode_token(token, 'username')
    if username is None:
        return jsonify({'message': 'miss token'}), 401
    if dbmanager.check_user(username):
        device_list = dbmanager.get_device(room_id)
        if len(device_list) > 0:
            return jsonify({'success': True, 'device': device_list}), 200
        else:
            return jsonify({'message': 'no data'}), 400
    return jsonify({'message': 'user does not exist'}), 400


@app.route('/api/control-device', methods=['POST'])
def api_control_device():
    access_token = request.headers['x-access-token']
    if access_token is None:
        return jsonify({'success': False, 'message': 'miss token'}), 400
    content = request.headers['Content-Type']
    if content == 'application/x-www-form-urlencoded':
        did = request.form.get('device_id')
        device = dbmanager.get_device_by_id(did)
        if device is None:
            return jsonify({'success': False, 'message': 'No find device'}), 400
        token = device['token']
        if request.form.get('operation_status') == 'true':
            command = {"80": "30"}
        else:
            command = {"80": "31"}
        result = apimanager.control_device(token, decode_token(token, 'home'), device['room_id'], device['device_type'],
                                           device['device_id'], str(command))
        print(result)
        if result == 'success':
            return jsonify({'success': True}), 200
        elif result == 'invalid token':
            return jsonify({'success': False, 'message': 'token expired'}), 400
        elif result == 'jwt expired':
            return jsonify({'success': False, 'message': 'token expired'}), 400
        else:
            return jsonify({'success': False, 'message': 'token expired'}), 400

    elif content == 'application/json':
        did = request.get_json()['device_id']
        device = dbmanager.get_device_by_id(did)
        if device is None:
            return jsonify({'success': False, 'message': 'No find device'}), 400
        token = device['token']
        if request.get_json()['operation_status']:
            command = {"80": "30"}
        else:
            command = {"80": "31"}
        result = apimanager.control_device(token, decode_token(token, 'home'), device['room_id'], device['device_type'],
                                           device['device_id'], str(command))

        if result == 'success':
            return jsonify({'success': True}), 200
        elif result == 'invalid token':
            return jsonify({'success': False, 'message': 'token expired'}), 400
        elif result == 'jwt expired':
            return jsonify({'success': False, 'message': 'token expired'}), 400
        else:
            return jsonify({'success': False, 'message': 'token expired'}), 400
    else:
        return jsonify({'message': '415 Unsupported Media Type'}), 415


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
