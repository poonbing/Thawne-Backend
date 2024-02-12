from flask_socketio import Namespace, emit, join_room, leave_room
from utils.data_class_model import *
from .utils import auth, db, get_top_messages, save_message, return_file, reflect_all_chats, get_signed_url
from utils.cryptography import generate_key, sha256_hash_bytes, encrypt_data
import uuid
import json



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
        # message = encrypt_data(json.dumps(message))
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
            # message = encrypt_data(json.dumps(message))
            emit('return_message_submission', message)
            _, message = get_top_messages(user_id, chat_id, security_level, password)
            # message = encrypt_data(json.dumps(message))
            emit('return_message_list', message, to=chat_id)
        else:
            # message = encrypt_data(json.dumps(message))
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
            # message = encrypt_data(json.dumps(levels))
            emit('return_filename_check', levels)
            return
        except:
            message = "Error occured."
            # message = encrypt_data(json.dumps(message))
            emit('error_filename_check', message)
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
                url = get_signed_url(filename)
                message = {"url":url, "password":file_password}
                # message = encrypt_data(json.dumps(message))
                emit('return_file_upload', message)
                message = {"user_id":user_id, "password":password, "filename":filename, "file_security":file_security}
                # message = encrypt_data(json.dumps(message))
                emit('queue_file', message, namespace="filescan")
                _, message = get_top_messages(user_id, chat_id, security_level, password)
                # message = encrypt_data(json.dumps(message))
                emit('return_message_list', message, to=chat_id)
            else:
                message = 'Error in handling message'
                # message = encrypt_data(json.dumps(message))
                emit('error_file_upload', message)
        else:
            message = granted_level[0]
            # message = encrypt_data(json.dumps(message))
            emit('inappropriate_level', message)

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
            message = "Incorrect credentials"
            # message = encrypt_data(json.dumps(message))
            emit('error_request_file', message)
        encrypted_password = sha256_hash_bytes(chat_id+file_password+password)
        if encrypted_password == file_password_hash:
            _, message = return_file(chat_id, password, file_security, filename)
            # message = encrypt_data(json.dumps(message))
            emit('return_request_file', message)
        else:
            message = "Incorrect password"
            # message = encrypt_data(json.dumps(message))
            emit('error_request_file', )
        
    def on_reflect_all_chats(self, data):
        user_id = data.get("userId")
        status, message = reflect_all_chats(user_id, data.get("password"))
        # message = encrypt_data(json.dumps(message))
        if status:
            emit('return_all_chats', message)
        else:
            emit('error_all_chats', message) 