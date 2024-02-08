import uuid
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

def verify_chat_user(user_id, chat_id, security_level, password):
    try:
        chat = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
        if not chat:
            return False, "Incorrect chat information."
        member_list = db.child("chats").child(chat_id).child(security_level).child("members").get(token=chat['idToken']).val()
        if user_id in member_list:
            return True, {user_id:member_list[user_id]}
        else:
            return False, "User not in the chat group."
    except Exception as e:
        return False, f"Error verifying chat user: {str(e)}"

def get_top_messages(user_id, chat_id, security_level, password):
    check, status = verify_chat_user(user_id, chat_id, security_level, password)
    if not check:
            return False, status
    try:
        chat = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
        message_list = db.child("chats").child(chat_id).child(security_level).child("chat_history").get(token=chat['idToken']).val()
        if password != 'false':
            if message_list:
                for message_data in message_list:
                    try:
                        message_list[message_data]["content"]["filename"] = decrypt_data(message_list[message_data]["content"], password)
                    except:
                        message_list[message_data]["content"] = decrypt_data(message_list[message_data]["content"], password)
        return True, message_list
    except Exception as e:
        return True, f"Chat does not have messages yet. {e}"
    
print(get_top_messages("UM77682", "O112748N", "Open", "false"))