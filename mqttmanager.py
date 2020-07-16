import json

import paho.mqtt.client as mqtt

from constant import MqttConstant
from dbmanager import update_name_device, update_status_device
from firestoremanager import update_data as update_firestore
from recognizedevice import train_model, recognize_device
import time


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
        client.loop_stop(False)


def on_message(client, userdata, msg):
    print('topic \"' + msg.topic + '\" published a message ')
    # print('message: ' + json.loads(msg.payload))
    spl = msg.topic.split('/')
    device_id = spl[5]
    packet = json.loads(msg.payload)  # convert string to json
    operation_status = packet.get('operation_status')
    if operation_status:
        characteristic = packet.get('characteristic', [])
        if len(characteristic) > 0:
            start = time.time()
            print(start)
            name = recognize_device(characteristic)
            time.sleep(1)
            end = time.time()
            print(end)
            print(end-start)
            print('device type: ' + name)
            update_name_device(device_id, name)
            update_firestore(device_id, {u'device_type': name, u'operation_status': operation_status})
        else:
            # no device
            update_name_device(device_id, 'No Device')
            update_firestore(device_id, {u'device_type': u'No Device', u'operation_status': operation_status})
            print('no device')
    else:
        update_firestore(device_id, {u'device_type': u'No Device', u'operation_status': operation_status})
    update_status_device(device_id, operation_status)


def subscribe(client, topics):
    topic_list = []
    for topic in topics:
        topic_list.append((topic, 0))
    client.subscribe(topic_list)


def subscribe_topics(token: str, topics: list):
    client = mqtt.Client(clean_session=True)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(username=token, password='*')
    client.connect(MqttConstant.host, MqttConstant.port, 60)
    subscribe(client, topics)
    client.loop_start()


def run(token):
    train_model()
    client = mqtt.Client(clean_session=True)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(username=token, password='*')
    client.connect(MqttConstant.host, MqttConstant.port, 60)
    subscribe(client, ['/testacc/9/TrongThuy/ElectricalSocket/#'])

    client.loop_forever()
    print('a')


if __name__ == '__main__':
    _token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlX2lkIjoieWN6a2dxYnh1dWdsN2g0dC12dG4yY2YydC10eDJsIiwiYXV0aGVudGljYXRvciI6InRlc3RhY2MiLCJob21lIjo5LCJyb29tIjpbMzYsMzddLCJyb29tX25hbWUiOlt7InJvb21faWQiOjM2LCJyb29tX25hbWUiOiJUcm9uZ1RodXkifSx7InJvb21faWQiOjM3LCJyb29tX25hbWUiOiJUaHV5VGVzdCJ9XSwiZGV2aWNlX3R5cGUiOlsiRWxlY3RyaWNhbFNvY2tldCJdLCJ0b3BpYyI6W3sidG9waWMiOiIvdGVzdGFjYy85L1Ryb25nVGh1eS9FbGVjdHJpY2FsU29ja2V0LyMiLCJwcml2aWxlZ2UiOjR9LHsidG9waWMiOiIvdGVzdGFjYy85L1RodXlUZXN0L0VsZWN0cmljYWxTb2NrZXQvIyIsInByaXZpbGVnZSI6NH1dLCJpYXQiOjE1OTM3NzIwOTcsImV4cCI6MTU5Mzg1ODQ5N30.FVEeFI4CfJ8L5wFl7pxLnoVQfAMktGmairLyecErhb6-J-XMtsChpRg_QdyAIpEF-Ub0AU8MBFBGIiTgHww2FA'
    _topic = ['/testacc/9/TrongThuy/ElectricalSocket/#']
    run(_token)
