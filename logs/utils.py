import pyrebase
from datetime import datetime
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

def log_event(user_id, password, type_of_offense, location, context):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    if not user:
        return False, "Incorrect User information, please retry."
    try:
        id_list = list(db.child("logs queue").shallow().get(user['idToken']).val())
        counter = str(int(max(id_list, key=lambda x: int(x))) + 1).zfill(6)
    except:
        counter = '000000'
    log = {
        "type of offense":type_of_offense,
        "timestamp":timestamp,
        "offender":user_id,
        "location of offense":location,
        "context of offense":context
    }
    try:
        db.child("logs queue").child(counter).update(log, user['idToken'])
    except:
        return False, "Error in logging"
    return True, "Log Queued"

def retrieve_log_queue(user_id, password):
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    if user:
        try:
            logs = db.child("logs queue").order_by_key().limit_to_first(40).get(token=user["idToken"]).val()
            return True, logs
        except:
            return True, "No logs in queue."
    else:
        return False, "Incorrect User Information"

def resolve_log_queue(user_id, password, id_list):
    result = {}
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    if user:
        logs = db.child("logs queue").get(token=user["idToken"]).val()
        for id in logs:
            if id in id_list:
                result[id] = logs[id]
                db.child("logs queue").child(id).remove(token=user["idToken"])
        db.child("logs history").update(result, token=user["idToken"])
        return True, "Logs resolved"
    else:
        return False, "Incorrect credentials"
            