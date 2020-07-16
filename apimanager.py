import json

import requests

from constant import token_base

base_url = 'https://sv-procon.uet.vnu.edu.vn:3000/api/services'


def get_device_list(token: str, home_id: str, room_id: str, device_type: str):
    url = base_url + '/devices?home_id={:s}&room_id={:s}&device_type={:s}'
    url = url.format(home_id, room_id, device_type)
    headers = {'x-access-token': token}
    res = requests.get(url=url, headers=headers)
    if res.json()['success']:
        data = res.json()['data']
        devices = []
        for _data in data:
            device_id = _data.get('device_id')
            device_type = _data.get('type_device')
            name = _data.get('name_device')
            room = _data.get('install_location')
            devices.append({'device_id': device_id, 'device_type': device_type, 'device_name': name, 'room_id': room})
        return devices
    else:
        # if res.json().get('reason', {}).get('message') in ['jwt expired', 'invalid signature']:
        return None


def get_device_data(token: str, home_id: str, room_id: str, device_type: str, device_id: str):
    url = base_url + '/get-device-data/home/{:s}/room/{:s}/device_type/{:s}/device_id/{:s}'
    url = url.format(home_id, room_id, device_type, device_id)
    headers = {'x-access-token': token}
    res = requests.get(url=url, headers=headers)
    print(json.dumps(res.json(), indent=4))


def control_device(token: str, home_id: int, room_id: int, device_type: str, device_id: str, command: str):
    url = base_url + '/devices/command'
    headers = {'x-access-token': token}
    data = {
        "home_id": home_id,
        "room_id": room_id,
        "device_type": device_type,
        "device_id": device_id,
        "command": command
    }
    res = requests.post(url=url, headers=headers, json=data).json()
    print(res)
    if res.get('success'):
        return 'success'
    else:
        return res.get('reason').get('message')


if __name__ == '__main__':
    # print(get_device_list(token_base, '9', '36', 'ElectricalSocket'))
    command_ = {"80": "30"}
    print(control_device(token_base, 9, 36, 'ElectricalSocket', '50:02:91:67:ec:de-0-35-1',
                         str(command_)))
