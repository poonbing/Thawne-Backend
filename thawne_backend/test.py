import uuid
from datetime import datetime
from cryptography import *
import pyrebase
from data_class_model import *

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

def logout(user_id, password):
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    new_status = {"login status":False}
    db.child("user logs").child(user['localId']).update(new_status, token=user['idToken'])
    return "yes"

def login_check(user_id, password):
    try:
        user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
        user_data = db.child("users").child(user['localId']).get(token=user['idToken']).val()
        if user_data:
            if user_data['status'] == 'Enabled':
                new_status = {"login status":True}
                db.child("user logs").child(user['localId']).update(new_status, token=user['idToken'])
                return True, "User successfully logged in"
            elif user_data["status"] == 'Disabled':
                return False, f"User account disabled, unable to login."
        else:
            return False, "Incorrect Username or Password."
    except Exception as e:
        return False, f"Error during login check: {str(e)}"

print(logout("UM77682", "poonbing@root"))