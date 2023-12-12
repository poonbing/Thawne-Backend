import uuid
from datetime import datetime
from cryptography import *
import pyrebase

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

def reflect_all_chats(user_id):
    return_dict = {}
    user_chats = db.child("users").child(user_id).child("chats").get().val()
    chats = db.child("chats").get().val()
    if user_chats and chats:
        for chat_id in user_chats:
            chat_name = chats[chat_id]["chat_name"]
            chat_level = user_chats[chat_id]["security level"]
            return_dict[chat_name] = {chat_level:chat_id}
        return True, return_dict
    else:
        return False, "Error in retrieving chats"

status, statement = reflect_all_chats("6cc260f0")
print(statement)
