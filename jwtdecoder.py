import jwt


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
        value = payload[key]
        return value
    except:
        return None

# payload = {'username': 'abc'}
# token1 = jwt.encode(payload, '').decode('utf-8')
# pay = jwt.decode(token1, verify=False)
# print(pay)
# #
# username = decode_token(token1, 'authenticator')
# insert_token(username, token1)

# print(jwt.decode(constant.token_base, verify=False))
