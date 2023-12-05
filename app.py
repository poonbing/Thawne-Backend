from flask import Flask
import pyrebase
from datetime import datetime
import uuid

app = Flask(__name__)

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

def login_check(user_id, password):
    try:
        user_data = db.child('users').child(user_id).get().val()
        if user_data and user_data["password"] == password:
            if user_data["status"] == "Enabled":
                return True, user_data.get('chats', {})
            elif user_data["status"] == "Disabled":
                return False, "User has been Disabled."
        else:
            return False, "Incorrect Password."
    except:
        return False, "User does not exist."

def verify_chat_user(user_id, chat_id, security_level, password):
    try:
        chat = db.child('chats').child(chat_id).child(security_level).child(password)
        member_list = chat.child("members").get().val()
        if user_id in member_list:
            return True, chat
        else:
            return False, "User not in chat group."
    except:
        return False, "Incorrect chat information."

def check_user_access(user_id, chat_id):
    user_access = db.child("users").child(user_id).child("chats").child(chat_id).child("access").get().val()
    return user_access

def get_top_messages(user_id, chat_id, security_level, password, message_count):
    check, status = verify_chat_user(user_id, chat_id, security_level, password)
    if check:
        access = check_user_access(user_id, chat_id)
        if access["read"]:
            try:
                messages = status.child("chat_history").limit_to_last(message_count).get().val()
            except:
                messages = status.child("chat_history").get().val()
            message_list = list(reversed(messages))
            return True, message_list
        else:
            return False, "User does not have permission to access this chat."
    else:
        return False, status

def save_message(user_id, chat_id, security_level, password, message_content):
    timestamp = int(datetime.utcnow().timestamp()*1000)
    check, status = verify_chat_user(user_id, chat_id, security_level, password)
    if check:
        access = check_user_access(user_id, chat_id)
        if access["write"]:
            new_message_count = int(status.child("message_count").get().val())+1
            new_message_id = chat_id+new_message_count
            new_message = {
                "id":new_message_id,
                "date":timestamp,
                "sent_from":user_id,
                "content":message_content
            }
            try:
                db.child('chats').child(chat_id).child(security_level).child(password).child("chat_history").push(new_message)
                db.child('chats').child(chat_id).child(security_level).child(password).child("message_count").update(new_message_count)
                return True, new_message_id
            except:
                return False, "Error in message saving."
        else:
            return False, "User does not have permission to send messages in this chat."
    else:
        return False, status

def get_all_chat(user_id):
    chat_list = db.child("users").child(user_id).child("chats").get().val()
    return chat_list

def augment_user(user_id, subject_user_id, keyword):
    if keyword in ["Enabled", "Disabled"]:
        user_level = db.child("users").child(user_id).child("level").get().val()
        if user_level == "admin":
            subject_user_level = db.child("users").child(subject_user_id).child("level").get().val()
            if subject_user_level != user_level:
                db.child("users").child(subject_user_id).child("status").update(keyword)
                return True, f"{subject_user_id} has been {keyword}."
            else:
                return False, f"{subject_user_id} is at the same priviledge level, thus cannot be {keyword}."
        else:
            return False, f"You do not have permissions to apply {keyword} to accounts."
        
def augment_user_chat_permission(user_id, subject_user_id, chat_id, keyword, status):
    if keyword in ["read", "write"]:
        user_level = db.child("users").child(user_id).child("level").get().val()
        if user_level == "admin":
            subject_user_level = db.child("users").child(subject_user_id).child("level").get().val()
            if subject_user_level != user_level:
                db.child("users").child(subject_user_id).child("chats").child(chat_id).child("access").child(keyword).update(status)
                return True, f"{subject_user_id}'s {keyword} permission to {chat_id} has been changed to {status}."
            else:
                return False, f"{subject_user_id} is at the same priviledge level, thus cannot be altered."
        else:
            return False, f"You do not have permissions to alter {keyword} permission of accounts."
    
def create_chat(user_id, chat_id, security_level, list_of_users, general_read, general_write):
    user_level = db.child("users").child(user_id).child("level").get().val()
    if user_level == "admin":
        if security_level == "Open":
            password = ""
        else:
            password = str(uuid.uuid4())[:12]
        db.child("chats").update(
            {chat_id:{
                security_level:{
                    password:{
                        "members": list_of_users,
                        "chat_history": {},
                        "message_count":0
                        },
                    }
                },
                "chat_name":"name"
            }
        )
        for user_id in list_of_users:
            chats = db.child("users").child(user_id).child("chats").get().val()
            chats[chat_id] = {"security level":security_level, "access":{"read":general_read, "write":general_write}}
            db.child("users").child(user_id).child("chats").update(chats)
        if security_level == "Open":
            return True, f"{chat_id} has been created. The security level is {security_level}."
        else:
            return True, f"{chat_id} has been created. The security level is {security_level}. The following is the password: {password}"
    else:
        return False, "User does not have permissions to create chats."

@app.route('/')
def hello():
    return True


if __name__ == '__main__':
    app.run(debug=True)