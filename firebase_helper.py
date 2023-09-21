from firebase_admin import credentials,initialize_app,storage,db
from urllib.request import urlretrieve
from flask import session
import time

cred = credentials.Certificate("./credentials.json")
initialize_app(cred,{'storageBucket':'test-3c6d6.appspot.com','databaseURL':'https://test-3c6d6-default-rtdb.asia-southeast1.firebasedatabase.app'})


bucket = storage.bucket()

def create_user(id):
    ref = db.reference('/requests/'+ id)
    ref.set({
        "sketch_url":"",
        "result_url":"",
        "sketch":0,
        "result":0
    })
    ref = db.reference('/users/'+id)
    ref.set({
        "status":0
    })

def get_active_users():
    ref = db.reference('/users')
    result = ref.get()
    return result

def upload_sketch(id,file_path,file_name):
    blob = bucket.blob(id+"/"+file_name)
    blob.upload_from_filename(file_path)
    ref = db.reference('/users/'+id)
    ref.set({
        "status":1
    })
    url = blob.generate_signed_url(int(time.time())+3600)
    ref = db.reference('/requests/'+ id)
    ref.update({
        "sketch_url":url,
        "sketch":1
    })

def upload_result(url,id):
    urlretrieve(url,"./temp_result.jpg")
    file = "./temp_result.jpg"
    blob = bucket.blob(id+"/result.jpg")
    blob.upload_from_filename(file)
    ref = db.reference('/users/'+id)
    ref.set({
        "status":2
    })
    ref = db.reference('/requests/'+ id)
    ref.update({
        "result_url":url,
        "result":1
    })

def get_urls():
    ref = db.reference('/requests/'+session['temp_user'])
    return ref.get()

def check_login(user,password):
    ref = db.reference("/admin").get()
    if ref['user'] == user and ref['password'] == password:
        return True
    else:
        return False


