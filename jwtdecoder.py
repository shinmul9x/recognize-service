import jwt
from dbmanager import insert_user

token1 = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlX2lkIjoidDQ2cjdjM2hpdGNqZmk3ay1zcXVwdjlrNC1mYng1IiwiYXV0aGVudGljYXRvciI6InRlc3RhY2MiLCJob21lIjo5LCJyb29tIjpbN10sImRldmljZV90eXBlIjpbIkFpckNvbmRpdGlvbmFsIl0sImlhdCI6MTU4NTkyMjYwMCwiZXhwIjoxNTg1OTQ0MjAwfQ.ClLissyPJtv_M0iLUHOunyHo3tnGI8hhRen1VQOHPzDc7N5JOtC1l7E1rz9FIof2peIsrrlGSMoIXdSns0HkBQ'


# def decode_token():
#     try:
#         payload = jwt.decode(token1, verify=False)
#         username = payload['authenticator']
#         homes = payload['home']
#         rooms = payload['room']
#         device_types = payload['device_type']
#         return username, homes, rooms, device_types
#     except:
#         return None, None, None, None


def decode_token(token: str, key: str):
    try:
        payload = jwt.decode(token, verify=False)
        username = payload[key]
        return username
    except:
        return None


# payload = {'username': 'abc'}
# token1 = jwt.encode(payload, '').decode('utf-8')
# pay = jwt.decode(token1, verify=False)
# print(pay)
#
# username = decode_token(token1, 'authenticator')
# insert_user(username, token1)
