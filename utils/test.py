import uuid
from datetime import datetime
from cryptography import generate_key
import pyrebase
from data_class_model import *
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


def stream_update(user_id):
    print(user_id)

def trigger_stream(user_id, chat_id, security_level, password):
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    my_stream = db.child("chats").child(chat_id).child(security_level).child("chat_history").stream(stream_update(user_id), stream_id=user_id, token=user["idToken"])


trigger_stream("UM77682", "S121057E", "Sensitive", "poonbing@root")