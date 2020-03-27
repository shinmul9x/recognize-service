from mysql import connector as mysql

from constant import DbConstant


def connect_db():
    return mysql.connect(**DbConstant.config)


def insert_token(token: str):
    query = 'INSERT INTO token_list(id, token) VALUES (%s, %s)'
    val = (None, token)

    db = connect_db()
    cur = db.cursor()
    cur.execute(query, val)
    db.commit()
    print(cur.rowcount, 'record(s) inserted')
    cur.close()
    db.close()


def delete_token(token: str):
    query = 'DELETE FROM token_list WHERE token = %s'
    val = (token,)

    db = connect_db()
    cur = db.cursor()
    cur.execute(query, val)
    db.commit()
    print(cur.rowcount, 'record(s) deleted')
    cur.close()
    db.close()


def insert_characteristic(**option):
    query = 'INSERT INTO device_name(id, name, token_id, device_id, authenticity) VALUES(%s, %s, %s, %s, %s)'
    val = (None, option['device_name'], option['token_id'], option['device_id'], option['authenticity'])

    db = connect_db()
    cur = db.cursor()
    cur.execute(query, val)
    db.commit()
    device_name_id = cur.lastrowid
    print(cur.rowcount, 'record(s) inserted with id is ', device_name_id)
    query = 'INSERT INTO data(id, amplitude, frequency, device_name_id) VALUES(%s, %s, %s, %s)'
    val = []
    amp = option['amplitude']
    freq = option['frequency']
    if freq is None:
        for i in range(len(amp)):
            val.append((None, amp[i], None, device_name_id))
    else:
        for i in range(len(amp)):
            val.append((None, amp[i], freq[i], device_name_id))
    cur.executemany(query, val)
    db.commit()
    print(cur.rowcount, 'record(s) inserted')
    cur.close()
    db.close()


def update_characteristic(id: str, authenticity: bool):
    pass
