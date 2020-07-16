from mysql import connector as mysql

from apimanager import get_device_list
from constant import DbConstant
from firestoremanager import push_data, update_data
from jwtdecoder import decode_token


def connect_db():
    return mysql.connect(**DbConstant.config)


def check_user(username: str):
    query = 'SELECT id FROM user WHERE username=%s'
    value = (username,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    result = cur.fetchone()
    cur.close()
    db.close()
    return result is not None


def get_user_id(username: str):
    # get id by username
    query = 'SELECT id FROM user WHERE username=%s'
    value = (username,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    result = cur.fetchone()
    # if username does not exist, insert this username into database
    if result is None:
        query = 'INSERT INTO user(username) VALUES(%s)'
        cur.execute(query, value)
        db.commit()
        result = cur.lastrowid
    else:
        result = result[0]
    cur.close()
    db.close()
    return result


def insert_home(user_id: int, home_id: int):
    # check whether or not this home exist
    query = 'SELECT * FROM home WHERE id=%s'
    value = (home_id,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    # if not exist, insert into database
    if cur.fetchone() is None:
        query = 'INSERT INTO home(id, user_id) VALUES(%s, %s)'
        value = (home_id, user_id)
        cur.execute(query, value)
        db.commit()
    cur.close()
    db.close()


def insert_room(home_id: int, room_id: int):
    # check whether or not this room exist
    query = 'SELECT id FROM room WHERE id=%s'
    value = (room_id,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    result = cur.fetchone()
    # if not exist, insert into database
    if result is None:
        query = 'INSERT INTO room(id, home_id) VALUES(%s, %s)'
        value = (room_id, home_id)
        cur.execute(query, value)
        db.commit()
    cur.close()
    db.close()


def insert_device(device_id: int, device_type: str, device_name: str, room_id: int, token: str):
    # check whether or not this device exist
    query = 'SELECT id FROM device WHERE device_id=%s AND room_id=%s'
    value = (device_id, room_id)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    result = cur.fetchone()
    # if not exist, insert into database
    if result is None:
        query = 'INSERT INTO device(device_id, device_type, device_name, room_id, token) VALUES(%s, %s, %s, %s, %s)'
        value = (device_id, device_type, device_name, room_id, token)
        cur.execute(query, value)
        db.commit()
        cur.close()
        db.close()
        return True
    cur.close()
    db.close()
    update_device(device_id, device_name, room_id, token)
    return False


def update_device(device_id: int, device_name: str, room_id: int, token: str):
    query = 'UPDATE device SET device_name=%s, room_id=%s, token=%s WHERE device_id=%s AND room_id IS NOT NULL'
    value = (device_name, room_id, token, device_id)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    db.commit()
    cur.close()
    db.close()


def insert_info_user(token: str):
    # get user id
    username = decode_token(token, 'authenticator')
    user_id = get_user_id(username)
    # insert home
    home_id = decode_token(token, 'home')
    insert_home(user_id, home_id)
    # insert rooms
    room = decode_token(token, 'room')
    for room_id in room:
        insert_room(home_id, room_id)
        # insert devices
        device_type = decode_token(token, 'device_type')
        for _type in device_type:
            devices = get_device_list(token, str(home_id), str(room_id), _type)
            if devices is not None:
                for device in devices:

                    if insert_device(device.get('device_id'), device.get('device_type'), device.get('device_name'),
                                     device.get('room_id'), token):
                        data = {
                            u'name': device.get('device_name'),
                            u'user_name': username,
                            u'device_type': 'No device',
                            u'device_id': device.get('device_id'),
                            u'operation_status': False
                        }
                        push_data(device.get('device_id'), data)
                    else:
                        data = {
                            u'name': device.get('device_name'),
                            u'device_type': 'No device'
                        }
                        update_data(device.get('device_id'), data)


def get_user_info(username: str):
    user_id = get_user_id(username)
    db = connect_db()
    cur = db.cursor()
    user_info = []
    query = 'SELECT id FROM home WHERE user_id=%s'
    value = (user_id,)
    cur.execute(query, value)
    home_list = cur.fetchall()
    for _hl in home_list:
        query = 'SELECT room.room_id ' + \
                'FROM room, token_room ' + \
                'WHERE room.id = token_room.room_id AND room.home_id = %s ' + \
                'GROUP BY room.room_id'
        value = (_hl[0],)
        cur.execute(query, value)
        room_list = cur.fetchall()
        room = []
        for _rl in room_list:
            room.append({'id': _rl[0]})
        user_info.append({'home_id': _hl[0], 'room': room})
    cur.close()
    db.close()
    return user_info


def get_home(username: str):
    query = 'SELECT home.id ' + \
            'FROM home, user ' + \
            'WHERE home.user_id = user.id AND user.username=%s'
    val = (username,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, val)
    result = cur.fetchall()
    cur.close()
    db.close()
    home = []
    for _home in result:
        home.append({'id': _home[0]})
    return home


def get_room(username: str, home_id: int):
    db = connect_db()
    cur = db.cursor()
    query = 'SELECT id ' + \
            'FROM room ' + \
            'WHERE home_id=%s'
    val = (home_id,)
    cur.execute(query, val)
    result = cur.fetchall()
    cur.close()
    db.close()
    if result is None:
        return None
    room = []
    for _room in result:
        room.append({'id': _room[0]})
    return room


def get_device(room_id: str):
    query = 'SELECT * FROM device WHERE room_id=%s'
    value = (room_id,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    result = cur.fetchall()
    cur.close()
    db.close()
    device_list = []
    for _device in result:
        device = {'id': _device[0], 'device_id': _device[1], 'device_type': _device[2], 'name': _device[3],
                  'device_name': _device[4], 'operation_status': bool(_device[5]), 'room_id': _device[8]}
        device_list.append(device)
    return device_list


def get_device_by_id(device_id):
    query = 'SELECT * FROM device WHERE id=%s'
    value = (device_id,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    result = cur.fetchone()
    cur.close()
    db.close()
    # device_list = []
    if result is None:
        return None
    device = {'device_id': result[1], 'device_type': result[2], 'token': result[7], 'room_id': result[8]}
    #     device_list.append(device)
    return device


def update_status_device(did: int, status: bool):
    query = 'UPDATE device SET operation_status=%s WHERE device_id=%s AND room_id IS NOT NULL'
    value = (status, did)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    db.commit()
    cur.close()
    db.close()


def update_name_device(did: str, name: str):
    query = 'UPDATE device SET name=%s WHERE device_id=%s AND room_id IS NOT NULL'
    value = (name, did)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    db.commit()
    cur.close()
    db.close()
    print('updated')


# insert_token(constant.token_base)
# info = get_user_info('testac')
# print(len(info))
# print(get_token('testac', 30))
# delete_token('fhjfhs')
# get_home('testa')
# print(get_room('testac', 9))


if __name__ == '__main__':
    topic = "/testacc/9/TrongThuy/ElectricalSocket/50:02:91:67:ec:de-0-35-1/data"
    # print(get_device(topic.split('/')[5]))
    # update_name_device('50:02:91:67:ec:de-0-35-1', 'abcd')
    print(get_device_by_id(1))
