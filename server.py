from flask import Flask, request
from flask_jsonpify import jsonify
from jwt import encode

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
        dbmanager.insert_token(token)
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


@app.route('/api/get-device-list/home/<home_id>/room/<room_id>', methods=['GET'])
def api_get_device_list(home_id, room_id):
    token = request.headers['x-access-token']
    username = decode_token(token, 'username')
    if username is None:
        return jsonify({'message': 'miss token'}), 401
    token_list = dbmanager.get_token(username, room_id)
    if len(token_list) == 0:
        return jsonify({'message': 'no token'}), 400
    device_list = []
    for _token in token_list:
        device_type = decode_token(_token, 'device_type')
        if device_type is None:
            continue
        for _type in device_type:
            _device = apimanager.get_device_list(_token, home_id, room_id, _type)
            if _device is not None:
                device_list.extend(_device)
    if len(device_list) > 0:
        return jsonify({'success': True, 'data': device_list}), 200
    else:
        return jsonify({'message': 'no data'}), 400


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
