from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from database_functions import *
import pyrebase


app = Flask(__name__)
CORS(app)


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
db = firebase.database()
storage = firebase.storage()


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    print(data)

    if "username" in data and "password" in data:
        username = data["username"]
        password = data["password"]

    # login_check(user_id = user_id,password = password)
    return jsonify({"token": "test123"})


@app.route("/verifychatuser", methods=["GET"])
def verify_user():
    user_id = request.args.get("uid")
    chat_id = request.args.get("cid")
    security_level = request.args.get("seclvl")
    password = request.args.get("pass")
    verify_chat_user(
        user_id=user_id,
        chat_id=chat_id,
        security_level=security_level,
        password=password,
    )


@app.route("/check_user_access", methods=["GET"])
def check_user_access():
    user_id = request.args.get("uid")
    chat_id = request.args.get("cid")
    check_user_access(user_id=user_id, chat_id=chat_id)


@app.route("/gettopmessages", methods=["GET"])
def get_top_messages():
    user_id = request.args.get("uid")
    chat_id = request.args.get("cid")
    security_level = request.args.get("seclvl")
    password = request.args.get("pass")
    message_count = request.args.get("msgc")
    get_top_messages(
        user_id=user_id,
        chat_id=chat_id,
        security_level=security_level,
        password=password,
        message_count=message_count,
    )


@app.route("/submitmessage", methods=["POST"])
def save_message():
    user_id = request.form["uid"]
    chat_id = request.form["cid"]
    security_level = request.form["seclvl"]
    password = request.form["pass"]
    message_content = request.form["msgcont"]

    save_message(
        user_id=user_id,
        chat_id=chat_id,
        security_level=security_level,
        password=password,
        message_content=message_content,
    )


@app.route("/getallchat", methods=["GET"])
def get_all_chat():
    user_id = request.form["uid"]
    get_all_chat(user_id=user_id)

    return 200


@app.route("/augmentuser", methods=["POST"])
def augment_user():
    user_id = request.form["uid"]
    subject_user_id = request.form["subuid"]
    keyword = request.form["key"]
    augment_user(user_id=user_id, subject_user_id=subject_user_id, keyword=keyword)

    return 200


@app.route("/augmentuserchatpermission", methods=["POST"])
def augment_user_chat_permission():
    user_id = request.form["uid"]
    subject_user_id = request.form["subuid"]
    chat_id = request.form["cid"]
    keyword = request.form["key"]
    status = request.form["status"]
    augment_user(
        user_id=user_id,
        subject_user_id=subject_user_id,
        chat_id=chat_id,
        keyword=keyword,
        status=status,
    )

    return 200


@app.route("/createchat", methods=["POST"])
def createChat():
    data = request.get_json()

    print(data)

    userId = data["userId"]
    chatName = data['chatName']
    chatDescription = data['chatDescription']
    securityLevel = data['securityLevel']
    listOfUsers = data['listOfUsers']
    generalRead = data['generalRead']
    generalWrite = data['generalWrite']
    
    status, msg = create_chat(user_id=userId, chat_name=chatName, chat_description=chatDescription, security_level=securityLevel, list_of_users=listOfUsers,  general_read=generalRead, general_write=generalWrite)
    

    return jsonify(msg)
    


if __name__ == "__main__":
    app.run(debug=True)
