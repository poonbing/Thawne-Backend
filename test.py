import uuid
from datetime import datetime
from cryptography import *
from database_functions import *
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

# print(login_check("c434be03", "poonbing@root"))
# print(verify_chat_user("c434be03", "3d5655a5-f32", "Top Secret", "7c0b69b0-2f8"))
# check_user_access("5d74d0f4", "3d5655a5-f32")
# get_top_messages("5d74d0f4", "3d5655a5-f32", "Top Secret", "7c0b69b0-2f8")
# print(save_message("UM77682", "O112748N", "Open", "false", "It is stinking up the whole office."))
# augment_user("5d74d0f4", "cefc6d16", "Enabled")
# augment_user_chat_permission("5d74d0f4", "cefc6d16", "3d5655a5-f32", "write", True)
# print(create_chat("UM77682", "poonbing@root", "InfoSec Project Development", "Very Secretive", "Top Secret", {"UA29907":"Lewis Tay", "UM68750":"Chua You Shen", "UU55518":"Snir Shalev"}))
# print(mass_user_creation({"Lee Boon Ping":{"password":"poonbing@root", "email":"poonbing@thawne.com", "level":"master"}, 
#                     "Lewis Tay":{"password":"tewislay@root", "email":"tewislay@thawne.com", "level":"admin"},
#                     "Chua You Shen":{"password":"youshen52@root", "email":"youshen52@thawne.com", "level":"master"},
#                     "Snir Shalev":{"password":"bobbysnir@root", "email":"bobbysnir@thawne.com", "level":"user"}}))
# mass_user_creation({"Sir Vincent":{"password":"root", "email":"root@thawne.com", "level":"user"}})
# print(reflect_all_chats("UM10775", "poonbing@root"))
# remove_user_from_chat("5d74d0f4", "3d5655a5-f32", "Top Secret", "7c0b69b0-2f8", "cefc6d16")
# add_user_to_chat("5d74d0f4", "3d5655a5-f32", "Top Secret", "7c0b69b0-2f8", "cefc6d16")
# delete_chat("5d74d0f4", "0468b201-468", "Open", "false")
# delete_user("5d74d0f4", "Leyau")
# obtain_chat_details("7064eef8-abd", "Top Secret", "df3beae9-a62")
# print(predict_class_level("Records of employee personal information"))

# user = user = auth.sign_in_with_email_and_password('O112748N'.lower()+"@thawne.com", generate_key('O112748N'.lower(), 'false'.lower())[:20])
# id_list = list(db.child('chats').child('O112748N').child('Open').child('chat_history').shallow().get(user['idToken']).val())
# print(max(id_list, key=lambda x: int(x.lstrip('0') or '0')))
print(get_top_messages('UM77682', 'O112748N', 'Open', 'false'))
# print(log_event('UM77682', 'poonbing@root', 'Sharing of sensitive information', 'S279123E', 'casuvbiaubviadsbv'))