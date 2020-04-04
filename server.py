from flask import Flask, request
from flask_jsonpify import jsonify
from recognizedevice import train_model, recognize_device
from constant import ApiConstant
import dbmanager

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
        option = {
            'device_name': device_name,
            'token_id': None,
            'device_id': None,
            'authenticity': None,
            'amplitude': characteristic,
            'frequency': None
        }
        dbmanager.insert_characteristic(**option)
        return jsonify({'label': device_name})
    else:
        return '415 Unsupported Media Type'


if __name__ == '__main__':
    app.run(ApiConstant.host, ApiConstant.port)
