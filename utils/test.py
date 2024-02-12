import uuid
import json
from datetime import datetime
from cryptography import generate_key
import pyrebase
from data_class_model import *
from cryptography import generate_key, encrypt_data, decrypt_data

# from thawne_backend.file_scan.filequeue import FileQueue
import PyPDF2

firebase_config = {
    "apiKey": "AIzaSyCslAm25aJkWReYOOXV8YNAGzsCVRLkxeM",
    "authDomain": "thawne-d1541.firebaseapp.com",
    "databaseURL": "https://thawne-d1541-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "thawne-d1541",
    "storageBucket": "thawne-d1541.appspot.com",
    "messagingSenderId": "101144409530",
    "appId": "1:101144409530:web:4f2663a71c5c204b4c5983",
    "measurementId": "G-N2NEVEDM49"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

dict = {"chat name":{"chat id": "chat password"},
"Chao Ang Mo":{"S531560E":"SE2185"},
"Very Secretive Channel":{"T255951T":"TT2943"},
"NYP SIT Club":{"O112748N":"false"},
}

def queue_chat_request(user_id, password, action, chat_name, chat_description=None, security_level=None, list_of_users=None, general_read=True, general_write=True):
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    level = db.child("users").child(user["localId"]).child("level").get(token=user["idToken"]).val()
    if level != "user":
        try:
            request_count = db.child("chat queue").child("queue_count").get(token=user["idToken"]).val() + 1
            queue_count = db.child("chat queue").child("request_count").get(token=user["idToken"]).val() + 1
        except:
            request_count = 1
            queue_count = 1
        request = {(request_count):{
                "action":action,
                "chat_name": chat_name,
            }}
        if action == "Create":
            request["chat_description"] = chat_description
            request[request_count]["security_level"] = security_level
            request[request_count]["list_of_users"] = list_of_users
            request[request_count]["general_read"] = general_read
            request[request_count]["general_write"] = general_write
        elif action == "Delete":
            pass
        db.child("chat queue").child("queue").update(request, token=user["idToken"])
        db.child("chat queue").child("queue_count").set(queue_count, token=user["idToken"])
        db.child("chat queue").child("request_count").set(request_count, token=user["idToken"])
        return True, "Queue Successfully Added."
    else:
        return False, "User not authorized to create chats."
    
print(queue_chat_request("UM77682", "poonbing@root", "create", "You suck"))