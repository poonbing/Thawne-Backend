from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from database_functions import *
import pyrebase
from flask_socketio import SocketIO
from data_class_model import *


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")


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



@socketio.on('login')
def login(data):
    print("trigger login")
    user_id = None
    password = None
    if "username" in data and "password" in data:
        user_id = data["username"]
        password = data["password"]
    result, message = login_check(user_id, password)
    print(f"result = {result}, message = {message}")
    if result:
        print("login success")
        socketio.emit('return_login', {"token": user_id})
    else:
        socketio.emit('error_login', {"error": message})


@socketio.on('verify_chat_user')
def verify_user(data):
    user_id = data.get("uid")
    chat_id = data.get("cid")
    security_level = data.get("seclvl")
    password = data.get("pass")
    state, message = verify_chat_user(
        user_id=user_id,
        chat_id=chat_id,
        security_level=security_level,
        password=password,
    )
    if state:
        socketio.emit('return_chat_user', message)
    socketio.emit('error_chat_user', message)


# @app.route("/check_user_access", methods=["GET"])
# def check_user_access():
#     user_id = request.args.get("uid")
#     chat_id = request.args.get("cid")
#     access = check_user_access(user_id=user_id, chat_id=chat_id)
#     return jsonify(access)


@socketio.on('get_message_list')
def GetTopMessages(data):
    user_id = data.get("userId")
    chat_id = data.get("chatId")
    security_level = data.get("securityLevel")
    password = data.get("pass")
    if password == False:
        password = 'false'
    state, message = get_top_messages(
        user_id=user_id,
        chat_id=chat_id,
        security_level=security_level,
        password=password,
    )
    print(user_id)
    print(message)
    if state:
        socketio.emit('return_message_list', message)
    socketio.emit('error_message_list', message)


@socketio.on('submit_message')
def saveMessage(data):
    user_id = data.get("userId")
    chat_id = data.get("chatId")
    security_level = data.get("securityLevel")
    password = data.get("chatPassword")
    message_content = data.get("message")
    if password == False:
        password = 'false'
    try:
        # file = data.get("file")
        # filename = data.get("filename")
        # file_security = data.get("file security")
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
    if state:
        state, message = get_top_messages(
            user_id=user_id,
            chat_id=chat_id,
            security_level=security_level,
            password=password,
        )
        socketio.emit('return_message_submission', message)
    socketio.emit('error_message_submission', message)

@socketio.on("check_filename")
def check_file_name(filename):
    try:
        granted_level = predict_class_level(filename)
        # dictionary = {1:"Open", 2:"Sensitive", 3:"Top Secret"}
        # result = dictionary
        # for key in dictionary:
        #     if dictionary[key] == granted_level:
        #         result.pop(key)
        #     elif dictionary[key] == granted_level:
        #         break
        socketio.emit('return_filename_check', granted_level)
    except:
        socketio.emit('error_filename_check', "Error occured.")

@socketio.on('reflect_all_chats')
def get_all_chat(data):
    status, message = reflect_all_chats(data.get("userId"), data.get("password"))
    if status:
        socketio.emit('return_all_chats', message)
    else:
        socketio.emit('error_all_chats', message)


# @app.route("/augmentuser", methods=["POST"])
# def augment_user():
#     user_id = request.form["uid"]
#     subject_user_id = request.form["subuid"]
#     keyword = request.form["key"]
#     state, message = augment_user(
#         user_id=user_id, subject_user_id=subject_user_id, keyword=keyword
#     )
#     if state:
#         return jsonify(message)
#     return jsonify(message)


# @app.route("/augmentuserchatpermission", methods=["POST"])
# def augment_user_chat_permission():
#     user_id = request.form["uid"]
#     subject_user_id = request.form["subuid"]
#     chat_id = request.form["cid"]
#     keyword = request.form["key"]
#     status = request.form["status"]
#     state, message = augment_user_chat_permission(
#         user_id=user_id,
#         subject_user_id=subject_user_id,
#         chat_id=chat_id,
#         keyword=keyword,
#         status=status,
#     )
#     if state:
#         return jsonify(message)
#     return jsonify(message)


@socketio.on('create_chat')
def createChat(data):
    userId = data["userId"]
    chatName = data["chatName"]
    chatDescription = data["chatDescription"]
    securityLevel = data["securityLevel"]
    listOfUsers = data["listOfUsers"]
    generalRead = data["generalRead"]
    generalWrite = data["generalWrite"]
    status, message = create_chat(
        user_id=userId,
        chat_name=chatName,
        chat_description=chatDescription,
        security_level=securityLevel,
        list_of_users=listOfUsers,
        general_read=generalRead,
        general_write=generalWrite,
    )
    if status:
        socketio.emit('return_chat_creation', message)
    socketio.emit('error_chat_creation', message)


if __name__ == "__main__":
    socketio.run(app)
