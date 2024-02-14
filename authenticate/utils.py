import pyrebase
from utils.cryptography import generate_key


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

def login_check(user_id, password):
    print(user_id, password)
    try:
        user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
        user_data = db.child("users").child(user['localId']).get(token=user['idToken']).val()
        if user_data:
            if user_data['status'] == 'Enabled':
                return True, db.child("users").child(user["localId"]).child("level").get(token=user["idToken"]).val()
            elif user_data["status"] == 'Disabled':
                return False, f"User account disabled, unable to login."
        else:
            return False, "Incorrect Username or Password."
    except Exception as e:
        return False, f"Error during login check: {str(e)}"
    
def logout(user_id, password):
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    db.child("user logs").child(user['localId']).child("login status").set(False, token=user['idToken'])
    
def verify_chat_user(user_id, chat_id, security_level, password):
    try:
        chat = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
        if not chat:
            print("Incorrect chat information.")
            return False, "Incorrect chat information."
        member_list = db.child("chats").child(chat_id).child(security_level).child("members").get(token=chat['idToken']).val()
        if user_id in member_list:
            print('Authenticated')
            return True, {user_id:member_list[user_id]}
        else:
            return False, "User not in the chat group."
    except Exception as e:
        return False, f"Error verifying chat user: {str(e)}"