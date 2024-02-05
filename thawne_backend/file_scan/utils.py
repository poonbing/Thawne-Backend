import nltk
import joblib
import pyrebase
from cryptography import *
from app import filequeue
import PyPDF2


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
storage = firebase.storage()

def predict_class_level(text):
    tokens = nltk.word_tokenize(text)
    preprocessed_text = " ".join(tokens)
    loaded_classifier = joblib.load('text_classifier_model.joblib')
    loaded_vectorizer = joblib.load('text_vectorizer.joblib')
    input_vector = loaded_vectorizer.transform([preprocessed_text])
    predicted_security_level = loaded_classifier.predict(input_vector)
    return predicted_security_level[0]

def filter_content(sentence):
    sentence.replace("\n", "")
    try:
        int(sentence)
        return False
    except:
        return sentence

def get_allowed(intended_level):
    if intended_level == "Open":
            allowed_levels = ["Open"]
    elif intended_level == "Sensitive":
        allowed_levels = ["Open", "Sensitive"]
    elif intended_level == "Top Secret":
        allowed_levels = ["Open", "Sensitive", "Top Secret"]
    return allowed_levels

def file_scan(user_id, password, filename, intended_level):
    # while not filequeue.is_empty():
        allowed_levels = get_allowed(intended_level)
        status, sentences = return_file(user_id, password, filename)
        if status:
            log = []
            unlog = []
            outcome = True
            counter = {
                "Open":0,
                "Sensitive":0,
                "Top Secret":0
            }
            for sentence in sentences:
                if filter_content(sentence):
                    level = predict_class_level(sentence)
                    counter[level] = counter[level] + 1 
                    if level not in allowed_levels:
                        log.append(sentence)
                        outcome = False
                    else:
                        unlog.append(sentence)
            if not outcome:
                return False, log, counter
            else:
                return True, log, counter

def return_file(user_id, password, filename):
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    if not user:
        return False, "Incorrect User information."
    try:
        # file_details = filename.split("/")
        # file = storage.child(f'files/{file_details[0]}/{file_details[1]}').download(file_details[2],user['idToken'])
        storage.child(filename).download(path="thawne_backend\templates", filename=filename, token=user['idToken'])
        with open(filename, 'rb') as file:
            text = extract_text_from_pdf(file)
        if os.path.exists(filename):
            os.remove(filename)
        return True, text.split(".")
    except Exception as e:
        return False, f"Error in obtaining file. {e}"
    
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text