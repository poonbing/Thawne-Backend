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


#create_chat("5d74d0f4", "NYP Bull Shitting", "Greatest Bullshitters", "Top Secret", ["6cc260f0", "cefc6d16", "893d318c"])
#save_message("5d74d0f4", "3d5655a5-f32", "Top Secret", "7c0b69b0-2f8", "Your mom stinky")
get_top_messages("5d74d0f4", "3d5655a5-f32", "Top Secret", "7c0b69b0-2f8")
