import json

import requests

from dbmanager import delete_token

base_url = 'https://sv-procon.uet.vnu.edu.vn:3000/api/sp/service'


def get_device_list(token: str, home_id: str, room_id: str, device_type: str):
    url = base_url + '/get-device-list/home/{:s}/room/{:s}/device_type/{:s}'
    url = url.format(home_id, room_id, device_type)
    headers = {'x-access-token': token}
    res = requests.get(url=url, headers=headers)
    if res.json()['success']:
        return res.json()['data']
    else:
        if res.json().get('reason', {}).get('message') in ['jwt expired', 'invalid signature']:
            delete_token(token)
        return None


def get_device_data(token: str, home_id: str, room_id: str, device_type: str, device_id: str):
    url = base_url + '/get-device-data/home/{:s}/room/{:s}/device_type/{:s}/device_id/{:s}'
    url = url.format(home_id, room_id, device_type, device_id)
    headers = {'x-access-token': token}
    res = requests.get(url=url, headers=headers)
    print(json.dumps(res.json(), indent=4))

# get_device_data(token1, '9', '7', 'AirConditional', '1111111111111')
