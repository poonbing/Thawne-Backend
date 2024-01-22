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
        user_id = data["username"]
        password = data["password"]

    result, message = login_check(user_id, password)
    print(message)

    if result:
        return jsonify({"token": user_id})
    else:
        return jsonify(message)


@app.route("/verifychatuser", methods=["POST", "GET"])
def verify_user():
    data = request.get_json()
    user_id = data.get("uid")
    chat_id = data.get("cid")
    security_level = data.get("seclvl")
    password = data.get("pass")

    print(data)

    state, message = verify_chat_user(
        user_id=user_id,
        chat_id=chat_id,
        security_level=security_level,
        password=password,
    )
    if state:
        return jsonify(success=True, message=message)
    return jsonify(success=False, message=message)


@app.route("/check_user_access", methods=["GET"])
def check_user_access():
    user_id = request.args.get("uid")
    chat_id = request.args.get("cid")
    access = check_user_access(user_id=user_id, chat_id=chat_id)
    return jsonify(access)


@app.route("/gettopmessages", methods=["GET", "POST"])
def GetTopMessages():
    data = request.get_json()
    user_id = data.get("userId")
    chat_id = data.get("chatId")
    security_level = data.get("securityLevel")
    password = data.get("pass")
    print(data)
    if password == False:
        password = 'false'
    # message_count = request.args.get("msgc")
    state, message = get_top_messages(
        user_id=user_id,
        chat_id=chat_id,
        security_level=security_level,
        password=password,
        # message_count=message_count,
    )
    print(f"State: {state}, Message: {message}")
    if state:
        return jsonify(success=True, message=message)
    return jsonify(success=False, message=message)


@app.route("/submitmessage", methods=["POST"])
def saveMessage():
    data = request.get_json()
    user_id = data.get("userId")
    chat_id = data.get("chatId")
    security_level = data.get("securityLevel")
    password = data.get("chatPassword")
    message_content = data.get("message")
    print(f"The data is {data}")
    print(f"{user_id} {chat_id} {security_level} {password} {message_content}")
    if password == False:
        password = 'false'

    try:
        # file = data.get("file")
        # filename = data.get("filename")
        # file_security = data.get("file security")
        scan = text_scanning(message_content)
        if scan:
            print(f"There is sensitive data being sent. {scan}")
        state, message = save_message(
            user_id=user_id,
            chat_id=chat_id,
            security_level=security_level,
            password=password,
            message_content=message_content,
            # file=file,
            # filename=filename,
            # file_security=file_security,
        )
    except:
        state, message = save_message(
            user_id=user_id,
            chat_id=chat_id,
            security_level=security_level,
            password=password,
            message_content=message_content,
        )

    print(f"State: {state}, Message: {message}")

    if state:
        state, message = get_top_messages(
            user_id=user_id,
            chat_id=chat_id,
            security_level=security_level,
            password=password,
        )
        return jsonify(message)
    return jsonify(data)


@app.route("/getallchat", methods=["GET", "POST"])
def get_all_chat():
    user_id = request.get_json()
    print(user_id)
    message = reflect_all_chats(user_id=user_id)

    return jsonify(message)


@app.route("/augmentuser", methods=["POST"])
def augment_user():
    user_id = request.form["uid"]
    subject_user_id = request.form["subuid"]
    keyword = request.form["key"]
    state, message = augment_user(
        user_id=user_id, subject_user_id=subject_user_id, keyword=keyword
    )
    if state:
        return jsonify(message)
    return jsonify(message)


@app.route("/augmentuserchatpermission", methods=["POST"])
def augment_user_chat_permission():
    user_id = request.form["uid"]
    subject_user_id = request.form["subuid"]
    chat_id = request.form["cid"]
    keyword = request.form["key"]
    status = request.form["status"]
    state, message = augment_user_chat_permission(
        user_id=user_id,
        subject_user_id=subject_user_id,
        chat_id=chat_id,
        keyword=keyword,
        status=status,
    )
    if state:
        return jsonify(message)
    return jsonify(message)


@app.route("/createchat", methods=["POST"])
def createChat():
    data = request.get_json()

    print(data)

    userId = data["userId"]
    chatName = data["chatName"]
    chatDescription = data["chatDescription"]
    securityLevel = data["securityLevel"]
    listOfUsers = data["listOfUsers"]
    generalRead = data["generalRead"]
    generalWrite = data["generalWrite"]

    message = create_chat(
        user_id=userId,
        chat_name=chatName,
        chat_description=chatDescription,
        security_level=securityLevel,
        list_of_users=listOfUsers,
        general_read=generalRead,
        general_write=generalWrite,
    )

    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
