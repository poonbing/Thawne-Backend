from flask_socketio import Namespace, emit, join_room, send, leave_room, rooms
from utils.data_class_model import *
from .utils import auth, db, get_top_messages, text_scanning, save_message, return_file, reflect_all_chats, get_signed_url
from utils.cryptography import generate_key, sha256_hash_bytes
import uuid



class ChatNamespace(Namespace):
    user_rooms = {}

    def on_get_message_list(self, data):
        user_id = data.get("userId")
        chat_id = data.get("chatId")
        security_level = data.get("securityLevel")
        password = data.get("pass")
        if password == False:
            password = 'false'
        state, message = get_top_messages(user_id, chat_id, security_level, password)
        if state:
            try:
                room_name = self.user_rooms[user_id]
                leave_room(room_name)
            except:
                pass
            join_room(chat_id)
            self.user_rooms[user_id] = chat_id
            emit('return_message_list', message)
        else:
            emit('error_message_list', message)


    def on_submit_message(self, data):
        user_id = data.get("userId")
        chat_id = data.get("chatId")
        security_level = data.get("securityLevel")
        password = data.get("chatPassword")
        message_content = data.get("message")
        if password == False:
            password = 'false'
        state, message = save_message(user_id, chat_id, security_level, password, message_content)
        if state:
            state, message = get_top_messages(user_id, chat_id, security_level, password,)
            emit('return_message_submission', message)
            _, message = get_top_messages(user_id, chat_id, security_level, password)
            emit('return_message_list', message, to=chat_id)
        else:
            emit('error_message_submission', message)
    
    def on_check_filename(self, filename):
        try:
            filename = filename.split('/')[-1]
            granted_level = predict_class_level(filename)
            levels = ["Top Secret", "Sensitive", "Open"]
            count = 0
            for level in levels:
                if granted_level == level:
                    levels = levels[count:]
                    break
                count += 1
            emit('return_filename_check', levels)
            return
        except:
            emit('error_filename_check', "Error occured.")
            return
    
    def on_file_upload(self, data):
        user_id = data.get('userId')
        chat_id = data.get('chatId')
        password = data.get('chatPassword')
        security_level = data.get('securityLevel')
        filename = data.get('fileName')
        file_security = data.get('fileSecurity')
        file_password = "false"
        filename = filename.split('/')[-1]
        url = get_signed_url(filename)
        granted_level = predict_class_level(filename)
        levels = ["Top Secret", "Sensitive", "Open"]
        count = 0
        for level in levels:
            if granted_level == level:
                levels = levels[count:]
                break
            count += 1
        print(levels)
        if file_security in levels:
            if password == False:
                password = 'False'
                encrypted_password = 'False'
            if file_security != "Open":
                file_password = filename[:1].upper() + filename[-1:].upper() + str(uuid.uuid4().int)[:4]
            status, _ = save_message(user_id, chat_id, security_level, password, False, True, filename, file_security, 'false')
            if status:
                emit('return_file_upload', {"url":url, "password":file_password}, headers={
             'Access-Control-Allow-Origin': 'http://localhost:3000',
             'Access-Control-Allow-Methods': ["GET", "PUT", "POST", "DELETE", "OPTIONS"],
             'Access-Control-Allow-Headers': 'Content-Type'
         })
                emit('queue_file', {"user_id":user_id, "password":password, "filename":filename, "file_security":file_security}, namespace="filescan")
                _, message = get_top_messages(user_id, chat_id, security_level, password)
                emit('return_message_list', message, to=chat_id)
            else:
                emit('error_file_upload', 'Error in handling message')
        else:
            emit('inappropriate_level', granted_level[0])

    def on_request_file(self, data):
        chat_id = data.get('chatId')
        password = data.get('password')
        security_level = data.get('securityLevel')
        message_id = data.get('messageId')
        filename = data.get('fileName')
        file_security = data.get('fileSecurity')
        file_password = data.get('filePassword')
        try:
            chat = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
            file_password_hash = db.child("chats").child(chat_id).child(security_level).child('chat_history').child(message_id).child('content').child('file_password').get(token=chat['idToken']).val()
        except:
            emit('error_request_file', "Incorrect credentials")
        encrypted_password = sha256_hash_bytes(chat_id+file_password+password)
        if encrypted_password == file_password_hash:
            file = return_file(chat_id, password, file_security, filename)
            emit('return_request_file', file)
        else:
            emit('error_request_file', "Incorrect password")
        
    def on_reflect_all_chats(self, data):
        user_id = data.get("userId")
        status, message = reflect_all_chats(user_id, data.get("password"))
        if status:
            emit('return_all_chats', message)
        else:
            emit('error_all_chats', message) 