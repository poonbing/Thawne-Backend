import uuid
from datetime import datetime
from cryptography import *
from database_functions import *
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

#login_check("5d74d0f4", "poonbing@root")
#verify_chat_user("5d74d0f4", "3d5655a5-f32", "Top Secret", "7c0b69b0-2f8")
#check_user_access("5d74d0f4", "3d5655a5-f32")
#get_top_messages("5d74d0f4", "3d5655a5-f32", "Top Secret", "7c0b69b0-2f8")
#save_message("5d74d0f4", "3d5655a5-f32", "Top Secret", "7c0b69b0-2f8", "Your mom stinky")
#augment_user("5d74d0f4", "cefc6d16", "Enabled")
#augment_user_chat_permission("5d74d0f4", "cefc6d16", "3d5655a5-f32", "write", True)
#create_chat("5d74d0f4", "NYP SIT Club", "Lmao", "Open", ["6cc260f0", "cefc6d16", "893d318c"])
#mass_user_creation({"Leyau":{"password":"root", "email":"root@thawne.com", "level":"user"}})
#reflect_all_chats("5d74d0f4")
#remove_user_from_chat("5d74d0f4", "3d5655a5-f32", "Top Secret", "7c0b69b0-2f8", "cefc6d16")
#add_user_to_chat("5d74d0f4", "3d5655a5-f32", "Top Secret", "7c0b69b0-2f8", "cefc6d16")
#delete_chat("5d74d0f4", "0468b201-468", "Open", "false")
#delete_user("5d74d0f4", "Leyau")
#obtain_chat_details("7064eef8-abd", "Top Secret", "df3beae9-a62")



#db.child("chats").child("3d5655a5-f32").child("Top Secret").child("7c0b69b0-2f8").update({"members":["5d74d0f4", "893d318c", "6cc260f0", "cefc6d16"]})