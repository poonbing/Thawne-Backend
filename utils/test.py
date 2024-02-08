import uuid
import json
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

dict = {"chat name":{"chat id": "chat password"},
"Chao Ang Mo":{"S531560E":"SE2185"},
"Very Secretive Channel":{"T255951T":"TT2943"},
"NYP SIT Club":{"O112748N":"false"},
}
