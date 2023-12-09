from flask import Flask
import pyrebase
from database_functions import *

app = Flask(__name__)

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



@app.route('/')
def hello():
    return True


if __name__ == '__main__':
    app.run(debug=True)