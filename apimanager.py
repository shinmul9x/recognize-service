import requests
import json

base_url = 'https://sv-procon.uet.vnu.edu.vn:3000/api/sp/service'
token1 = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlX2lkIjoidDQ2cjdjM2hpdGNqZmk3ay1zcXVwdjlrNC1mYng1IiwiYXV0aGVudGljYXRvciI6InRlc3RhY2MiLCJob21lIjo5LCJyb29tIjpbN10sImRldmljZV90eXBlIjpbIkFpckNvbmRpdGlvbmFsIl0sImlhdCI6MTU4NTkyMjYwMCwiZXhwIjoxNTg1OTQ0MjAwfQ.ClLissyPJtv_M0iLUHOunyHo3tnGI8hhRen1VQOHPzDc7N5JOtC1l7E1rz9FIof2peIsrrlGSMoIXdSns0HkBQ'


def get_device_list(token: str, home_id: str, room_id: str, device_type: str):
    url = base_url + '/get-device-list/home/{:s}/room/{:s}/device_type/{:s}'
    url = url.format(home_id, room_id, device_type)
    headers = {'x-access-token': token}
    res = requests.get(url=url, headers=headers)
    if res.json()['success']:
        print(type(res.json()['data']))
        return res.json()['data']
    else:
        return None


def get_device_data(token: str, home_id: str, room_id: str, device_type: str, device_id: str):
    url = base_url + '/get-device-data/home/{:s}/room/{:s}/device_type/{:s}/device_id/{:s}'
    url = url.format(home_id, room_id, device_type, device_id)
    headers = {'x-access-token': token}
    res = requests.get(url=url, headers=headers)
    print(json.dumps(res.json(), indent=4))


# get_device_data(token1, '9', '7', 'AirConditional', '1111111111111')
