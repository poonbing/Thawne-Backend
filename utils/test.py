import uuid
import json
from datetime import datetime
from cryptography import generate_key
import pyrebase
from data_class_model import *
from cryptography import generate_key, encrypt_data, decrypt_data
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

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

server_account = {
  "type": "service_account",
  "project_id": "thawne-d1541",
  "private_key_id": "af8b057fdcc05e5505ce0ae3b8f7340fe724e954",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCbJ6jDpnZZQlVe\ni5ZboeWBnVtCCSMPldfXFjMqJMgu2pqF8HHCxX4qvsarIJ9ErVw+ECJ+6t8cyZg0\nZAXP0MS+r4uYQbci7OGTzB5X3r6UzmV4XbfixqyvNbjBgKo0dkMhYktzCBumHtKi\nGWoIDhVR/JWCcnQQuXfSuCt0ZpDJZD9lJXlpa38cshAIJ0tT7xH/06l6RD1CLLMU\nybC8nlzdWDeWPFYhdqmxlWYIjSN6SnDnKQcdu9/Nd1g1Jy18g58Mpis21Ja3zrwk\n13VkgiR1eXYNZJSo4uhxrPhHwTkWhexxjHu90WJm+J47VyVpnk/wCDvA7giqj9pw\nojcHwRJjAgMBAAECggEANAo1z0W+jUqz8o20JVDkdzhtuvTwlxIlvoU6LQkAQcLd\nsE4JAhCWtESfwxcihHj3JvPndhVWN0QgsnXYAy+dRe4ATtW/1M2KDbYZeVSDLMsb\neqdIfZ4wnmXQ7co3jHgcJQ7gipkuGOZetLL8fu4mVYT4KrQz3MYwe/N808JxDrL0\n4sMg8+U4ZXUyF6HXnTpNhw6heuVzJ1jT/TIAfxcS/W6WW23LXQr5f4Ju2qtyrkdC\nq2gkoH9fXzDuJK07NdH/v5jpBs9z924tA40y/5tBM3OQlpWcXaMHJ/7DI7HjlpVF\n4Jwrwu4POuWgZMTixcGekLo/hdxNT4wVDi7B2RFSaQKBgQDJkP0KrJ5c3GSd9DWc\nv4eATUPSTXHq6/ybcxJOa24exknssPOqg4KsHIOMuZ97oL++EPYv3E4oO+cgqDLb\nwC5qTyPDKxbRNfswtgTOP0mWhTepaZh8pXCWXfwkuCZ4+OuYDt5jFvo7kP1bWE40\nnWzrR4CQz6i1ciVbfDu6lVxGWwKBgQDFDhR2dWiJZiy8nwL3weyuhfv/ee58viFJ\nP/hihRa2lkKUl6Md6g6JmTF5wBooSWpbmWbqjrTn3U5yfxLYXVmkdHUAEP/xFqIq\nZPw2LhAvbvDaMDroVkf1yuFBYP8JvLVcXsoowdabuRhJM0YQovYC8ueMMgIMjx91\nYmCO0JvymQKBgQCI5gdmm4zHJwzTVsye1FqUYmXAzMalNngPoBz70+0ry6Ljtd8Y\nnU8/0/Hovx25Wpk/3sdGBEu0+dJllLdOFv2vSGbSpE5P82jSUZ178vHo4DvIvSZK\n6hZImjapPcUrfmyMjvStuipkEHpy8svS4mTae2qvb8p2ybrjosHyXIUaZwKBgBTL\ne5VUpod5ZNcy4JlMubFhKkq3j1dSqSiVu5yJ9u+lw7jyl6AchxQ2OmZiw1/k/3hT\nI+00yhp93D1w84gpscANGhu7r4a9oLdgmM0O515aEsiztkO2dzmVA1hm6AMbCviI\neET8z6z3R3zSEF7JE7UT9SNyU40HvYYhr5bipNJhAn9rYpUXNIow9n7uaMETU6Jn\nKty6DThX3eUP05it8pX/QvxgyqL0eADl/AzleiS3reIje+p92B9k44W26mDHmSia\nZ+qhpG+wxPWn2XVM545SvprC6u4bFmBvWv/Yef8Y3wocaJphyXckTH9f9xaZ4IJg\nYixvnR5XACTB/jn/YWdi\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-l09e1@thawne-d1541.iam.gserviceaccount.com",
  "client_id": "107836406402812014593",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-l09e1%40thawne-d1541.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
auth = firebase.auth()
pyrestorage = firebase.storage()
cred = credentials.Certificate(server_account)
firebase_admin.initialize_app(cred)

dict = {"chat name":{"chat id": "chat password"},
"Chao Ang Mo":{"S531560E":"SE2185"},
"Very Secretive Channel":{"T255951T":"TT2943"},
"NYP SIT Club":{"O112748N":"false"},
}