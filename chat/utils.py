import pyrebase
from utils.cryptography import generate_key, encrypt_data, decrypt_data
import re
from datetime import datetime
import nltk
import joblib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

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
auth = firebase.auth()
db = firebase.database()
pyrestorage = firebase.storage()
cred = credentials.Certificate(server_account)
firebase_admin.initialize_app(cred)


def verify_chat_user(user_id, chat_id, security_level, password):
    try:
        chat = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
        if not chat:
            return False, "Incorrect chat information."
        member_list = db.child("chats").child(chat_id).child(security_level).child("members").get(token=chat['idToken']).val()
        if user_id in member_list:
            return True, {user_id:member_list[user_id]}
        else:
            return False, "User not in the chat group."
    except Exception as e:
        return False, f"Error verifying chat user: {str(e)}"

def get_top_messages(user_id, chat_id, security_level, password):
    check, status = verify_chat_user(user_id, chat_id, security_level, password)
    if not check:
            return False, status
    try:
        chat = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
        message_list = db.child("chats").child(chat_id).child(security_level).child("chat_history").get(token=chat['idToken']).val()
        # if password != 'false':
        #     for message_data in message_list:
        #         message_data["content"] = decrypt_data(message_data["content"], password)
        return True, message_list
    except Exception as e:
        return True, f"Chat does not have messages yet. {e}"
    
def text_scanning(text):
    sensitive_data = [
    r'^[SFTG]\d{7}[A-Z]$', #NRIC
    r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$',  #IPv4
    r'^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$',  #Mastercard
    r'\b([4]\d{3}[\s]\d{4}[\s]\d{4}[\s]\d{4}|[4]\d{3}[-]\d{4}[-]\d{4}[-]\d{4}|[4]\d{3}[.]\d{4}[.]\d{4}[.]\d{4}|[4]\d{3}\d{4}\d{4}\d{4})\b', #Visa
    r'^3[47][0-9]{13}$',  #Amex
    r'\b[\w.-]{0,25}@(yahoo|hotmail|gmail)\.com\b' #Email
    ]
    words = text.split()  # Split the sentence into words
    for word in words:
        for pattern in sensitive_data:
            search = re.search(pattern, word, re.IGNORECASE)
            if search:
                matched_word = search.group()
                print('Matched:', matched_word)
                return matched_word
            
def save_message(user_id, chat_id, security_level, password, message_content, file=False, filename=False, file_security=False, file_password=False):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    check, status = verify_chat_user(user_id, chat_id, security_level, password)
    if not check:
        return False, status
    try:
        chat = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
        chat_info = db.child("chats").child(chat_id).child(security_level).get(token=chat['idToken']).val()
        new_message_count = str(int(chat_info["message_count"]) + 1).zfill(6)
        new_message_id = f"{chat_id}{new_message_count}"
        new_message = {
            "id": new_message_id,
            "date": timestamp,
            "sent_from": {user_id: status[user_id]},
        }
        if message_content:
            if password != 'false':
                message_content = encrypt_data(message_content, password)
            new_message['content'] = message_content
        if file:
            new_message["content"] = {
                "filename": filename,
                "file_security": file_security,
                "file_password": file_password
            }
        try:
            message_list = chat_info["chat_history"]
            message_list[new_message_count] = new_message
        except:
            message_list = {new_message_count:new_message}
        db.child("chats").child(chat_id).child(security_level).child("chat_history").set(message_list, token=chat['idToken'])
        db.child("chats").child(chat_id).child(security_level).child("message_count").set(new_message_count, token=chat['idToken'])
        return True, new_message_id
    except Exception as e:
        return False, f"Error in message saving.{e}"
    
def store_file(chat_id, password, filename, file, file_security):
    user = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
    if not user:
        return False, "Incorrect User information."
    try:
        filepath = f'files/{chat_id}/{file_security}/{filename}'
        pyrestorage.child(filepath).put(file, user['idToken'])
        return True, "File upload successful."
    except Exception as e:
        return False, f"Error in file upload: {e}"

def return_file(chat_id, password, file_security, filename):
    user = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
    if not user:
        return False, "Incorrect User information."
    try:
        file = pyrestorage.child(f'files/{chat_id}/{file_security}/{filename}').download(user['idToken'])
        return True, file
    except:
        return False, "Error in obtaining file."
    
def reflect_all_chats(user_id, password):
    return_list = []
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    user_chats = db.child("users").child(user['localId']).child("chats").get(token=user['idToken']).val()
    if user_chats:
        for chat_id in user_chats:
            chat_dict = {}
            chat_dict["chat_id"] = chat_id
            chat_dict["chat_name"] = user_chats[chat_id]["chat_name"]
            chat_dict["security_level"] = user_chats[chat_id]["security_level"]
            return_list.append(chat_dict)
        return True, return_list
    else:
        return False, "Error in retrieving chats"

def predict_class_level(text):
    tokens = nltk.word_tokenize(text)
    preprocessed_text = " ".join(tokens)
    loaded_classifier = joblib.load('filename_classifier_model.joblib')
    loaded_vectorizer = joblib.load('filename_vectorizer.joblib')
    input_vector = loaded_vectorizer.transform([preprocessed_text])
    predicted_security_level = loaded_classifier.predict(input_vector)
    return predicted_security_level

def get_signed_url(filename):
    bucket = storage.bucket("thawne-d1541.appspot.com")
    blob = bucket.blob(filename)
    url = blob.generate_signed_url(version="v4", expiration=0, method="PUT")
    return url