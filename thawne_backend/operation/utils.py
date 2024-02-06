import pyrebase
from datetime import datetime
import uuid
from cryptography import *

firebase_config = {
    "apiKey": "AIzaSyCslAm25aJkWReYOOXV8YNAGzsCVRLkxeM",
    "authDomain": "thawne-d1541.firebaseapp.com",
    "databaseURL": "https://thawne-d1541-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "thawne-d1541",
    "storageBucket": "thawne-d1541.appspot.com",
    "messagingSenderId": "101144409530",
    "appId": "1:101144409530:web:4f2663a71c5c204b4c5983",
    "measurementId": "G-N2NEVEDM49",
}


firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

def create_chat(user_id, password, chat_name, chat_description, security_level, list_of_users, general_read=True, general_write=True,):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    chat_id = security_level[:1].upper() + str(uuid.uuid4().int)[:6] + security_level[-1:].upper()
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    user_info = db.child("users").child(user['localId']).get(token=user['idToken']).val()
    user_level = user_info["level"]
    if user_level not in ["admin", "master"]:
        return False, "User does not have permissions to create chats."
    if security_level == "Open":
        password = 'false'
    elif security_level in ["Sensitive", "Top Secret"] and user_level == "admin":
        return False, "User does not have permissions to create Sensitive or Top Secret chats.",
    else:
        password = security_level[:1].upper() + security_level[-1:].upper() + str(uuid.uuid4().int)[:4] 
    creator = user_info["username"]
    list_of_users[user_id] = creator
    chat_data = {
        chat_id: {
            security_level:{
                    "chat_history":{},
                    "members": list_of_users,
                    "member_count": len(list_of_users),
                    "message_count": 0,
                },
            "chat_name": chat_name,
            "creation_date": timestamp,
            "chat_description": chat_description,
            "creator": creator,
        }
    }
    db.child("chats").update(chat_data, token=user['idToken'])
    auth.create_user_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
    users = db.child("users").get(token=user['idToken']).val()
    for uid in users:
        name = users[uid]["username"]
        if name in list_of_users.values():
            item = {"chat_name":chat_name,
                    "security_level": security_level,
                    "access": {"read": general_read,
                    "write": general_write},}
            db.child("users").child(uid).child("chats").child(chat_id).update(item, token=user['idToken'])
    if security_level == "Open":
        return True, f"{chat_id} has been created by {creator}. The security level is {security_level}."
    else:
        return True, f"{chat_id} has been created by {creator}. The security level is {security_level}. The following is the password: {password}"

def delete_chat(user_id, password, chat_id):
    try:
        user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
        if db.child("users").child(user["localId"]).child("level").get(user["idToken"]).val() == "Master":
            user_list = db.child("users").get(user["idToken"]).val()
            for uid in user_list:
                if chat_id in user_list[uid]["chats"]:
                    db.child("users").child(uid).child("chats").child(chat_id).remove(user["idToken"])
            db.child("chats").child(chat_id).remove(user["idToken"])
            return True, "Chat has been removed"
        else:
            return False, "Invalid User Level."
    except:
        return False, "Error in removing chat"