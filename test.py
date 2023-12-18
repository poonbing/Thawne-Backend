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



def create_chat(user_id, chat_name, chat_description, security_level, list_of_users, general_read=True, general_write=True):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    chat_id = str(uuid.uuid4())[:12]
    user_level = db.child("users").child(user_id).child("level").get().val()
    if user_level not in ["admin", "master"]:
        return False, "User does not have permissions to create chats."
    if security_level == "Open":
        password = True
    elif security_level in ["Sensitive", "Top Secret"] and user_level == "admin":
        return False, "User does not have permissions to create Sensitive or Top Secret chats."
    else:
        password = str(uuid.uuid4())[:12]
    creator = db.child("users").child(user_id).get().val()["username"]
    chat_data = {
        chat_id: {
            security_level: {
                password: {
                    "members": list_of_users,
                    "chat_history": {},
                    "message_count": 0,
                },
            },
            "chat_name": chat_name,
            "creation_date": timestamp,
            "chat_description": chat_description,
            "creator": creator,
        }
    }
    db.child("chats").update(chat_data)
    list_of_users.append(user_id)
    for user in list_of_users:
        user_chats = db.child("users").child(user).child("chats").get().val() or {}
        user_chats[chat_id] = {"security level": security_level, "access": {"read": general_read, "write": general_write}}
        db.child("users").child(user).child("chats").update(user_chats)
    if security_level == "Open":
        return True, f"{chat_id} has been created by {creator}. The security level is {security_level}."
    else:
        return True, f"{chat_id} has been created by {creator}. The security level is {security_level}. The following is the password: {password}"

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

status1, statement1 = create_chat("6cc260f0", "NYP SIT", "Dogshit Scheduling", "Open", ["893d318c", "cefc6d16", "5d74d0f4"])
status, statement = reflect_all_chats("893d318c")
print(statement)
