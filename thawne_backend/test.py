import uuid
from datetime import datetime
from cryptography import *
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


def predict_filename_level(text):
    tokens = nltk.word_tokenize(text)
    preprocessed_text = " ".join(tokens)
    loaded_classifier = joblib.load('filename_classifier_model.joblib')
    loaded_vectorizer = joblib.load('filename_vectorizer.joblib')
    input_vector = loaded_vectorizer.transform([preprocessed_text])
    predicted_security_level = loaded_classifier.predict(input_vector)
    return predicted_security_level

print(predict_class_level('Unclassified_Project_Overview_for_Public_Viewing'))