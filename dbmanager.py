from mysql import connector as mysql

from constant import DbConstant
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
    query = 'SELECT id FROM user WHERE username=%s'
    value = (username,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    result = cur.fetchone()
    if result is None:
        query = 'INSERT INTO user(id, username) VALUES(%s, %s)'
        value = (None, username)
        cur.execute(query, value)
        db.commit()
        result = cur.lastrowid
    else:
        result = result[0]
    cur.close()
    db.close()
    return result


def insert_home(user_id: int, home_id: int):
    query = 'SELECT * FROM home WHERE id=%s'
    value = (home_id,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    if cur.fetchone() is None:
        query = 'INSERT INTO home(id, user_id) VALUES(%s, %s)'
        value = (home_id, user_id)
        cur.execute(query, value)
        db.commit()
    cur.close()
    db.close()


def get_room_id(home_id: int, room_id: int):
    query = 'SELECT id FROM room WHERE room_id=%s AND home_id IS NOT NULL'
    value = (room_id,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    result = cur.fetchone()
    if result is None:
        query = 'INSERT INTO room(id, room_id, home_id) VALUES(%s, %s, %s)'
        value = (None, room_id, home_id)
        cur.execute(query, value)
        db.commit()
        result = cur.lastrowid
    else:
        result = result[0]
    cur.close()
    db.close()
    return result


def insert_token_room(token_id: int, room_id: int):
    query = 'SELECT * FROM token_room WHERE token_id=%s AND room_id=%s'
    value = (token_id, room_id)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    if cur.fetchone() is None:
        query = 'INSERT INTO token_room(id, token_id, room_id) VALUES(%s, %s, %s)'
        value = (None, token_id, room_id)
        cur.execute(query, value)
        db.commit()
    cur.close()
    db.close()


def insert_token(token: str):
    query = 'SELECT id FROM token_list WHERE token=%s'
    value = (token,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    result = cur.fetchone()
    if result is None:
        user_id = get_user_id(decode_token(token, 'authenticator'))
        query = 'INSERT INTO token_list(id, token, user_id) VALUES(%s, %s, %s)'
        value = (None, token, user_id)
        cur.execute(query, value)
        db.commit()
        token_id = cur.lastrowid
        home_id = decode_token(token, 'home')
        insert_home(user_id, home_id)
        room = decode_token(token, 'room')
        for room_id in room:
            insert_token_room(token_id, get_room_id(home_id, room_id))
    cur.close()
    db.close()


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
    query = 'SELECT home.id ' + \
            'FROM home, user ' + \
            'WHERE home.user_id = user.id AND user.username=%s AND home.id=%s'
    val = (username, home_id)
    cur.execute(query, val)
    if cur.fetchone() is None:
        cur.close()
        db.close()
        return None
    query = 'SELECT room.room_id ' + \
            'FROM room, token_room ' + \
            'WHERE room.id = token_room.room_id AND room.home_id = %s ' + \
            'GROUP BY room.room_id'
    val = (home_id,)
    cur.execute(query, val)
    room_list = cur.fetchall()
    cur.close()
    db.close()
    room = []
    for _rl in room_list:
        room.append({'id': _rl[0]})
    return room


def get_token(username: str, room_id: int):
    query = 'SELECT tl.token ' + \
            'FROM token_list AS tl, token_room AS tr, room AS r, user AS u ' + \
            'WHERE tl.id = tr.token_id AND tr.room_id = r.id AND u.id=tl.user_id AND r.room_id = %s AND u.username=%s'
    value = (room_id, username)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, value)
    result = cur.fetchall()
    cur.close()
    db.close()
    token = []
    for _r in result:
        token.append(_r[0])
    return token


def delete_token(token: str):
    query = 'DELETE FROM token_list WHERE token=%s'
    val = (token,)
    db = connect_db()
    cur = db.cursor()
    cur.execute(query, val)
    db.commit()
    cur.close()
    db.close()


# insert_token(constant.token_base)
# info = get_user_info('testac')
# print(len(info))
# print(get_token('testac', 30))
# delete_token('fhjfhs')
# get_home('testa')
# print(get_room('testac', 9))
