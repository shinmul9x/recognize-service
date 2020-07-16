import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading

# Use a service account
cred = credentials.Certificate('recognize-device-firebase-adminsdk-6exao-643274799a.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def push_data(device_id: str, data):
    # delete document if existed
    delete_data(device_id)
    db.collection(u'devices').add(data)


def update_data(device_id: str, data):
    docs = db.collection(u'devices').where(u'device_id', u'==', device_id).stream()
    if docs is not None:
        for doc in docs:
            updater = db.collection(u'devices').document(doc.id)
            updater.update(data)


def delete_data(device_id: str):
    docs = db.collection(u'devices').where(u'device_id', u'==', device_id).stream()
    if docs is not None:
        for doc in docs:
            db.collection(u'devices').document(doc.id).delete()

# # Create an Event for notifying main thread.
# callback_done = threading.Event()
#
#
# # Create a callback on_snapshot function to capture changes
# def on_snapshot(doc_snapshot, changes, read_time):
#     for doc in doc_snapshot:
#         print(f'Received document snapshot: {doc.id}')
#     callback_done.set()
#
#
# doc_ref = db.collection(u'devices')
#
# # Watch the document
# doc_watch = doc_ref.on_snapshot(on_snapshot)

if __name__ == '__main__':
    # doc_ref = db.collection(u'users').document(u'alove')
    # users_ref = db.collection(u'users')
    # docs = users_ref.get()
    #
    # for doc in docs:
    #     print(f'{doc.id} => {doc.to_dict()}')

    data_ = {
        'operation_status': True,
        'device_name': 'Sạc điện thoai',
        'username': 'testacc'
    }
    data2 = {'operation_status': False}
    update_data('50:02:91:67:ec:de-0-35-1', data2)
