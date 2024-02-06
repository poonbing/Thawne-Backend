from flask_socketio import Namespace, emit
from data_class_model import *
from .utils import auth, db, get_top_messages, text_scanning, save_message, return_file, reflect_all_chats, get_signed_url
from cryptography import generate_key, sha256_hash_bytes
import uuid

class ChatNamespace(Namespace):
    def on_get_message_list(self, data):
        user_id = data.get("userId")
        chat_id = data.get("chatId")
        security_level = data.get("securityLevel")
        password = data.get("pass")
        if password == False:
            password = 'false'
        state, message = get_top_messages(user_id, chat_id, security_level, password,)
        if state:
            emit('return_message_list', message)
            return
        emit('error_message_list', message)
        return

    def on_submit_message(self, data):
        user_id = data.get("userId")
        chat_id = data.get("chatId")
        security_level = data.get("securityLevel")
        password = data.get("chatPassword")
        message_content = data.get("message")
        if password == False:
            password = 'false'
        scan = text_scanning(message_content)
        if scan:
            emit('error_message_submission', "Sensitive information detected")
            return
        try:
            filename = data.get("filename")
            file_security = data.get("file security")
            state, message = save_message(user_id, chat_id, security_level, password, message_content, True, filename, file_security,)
        except:
            state, message = save_message(user_id, chat_id, security_level, password, message_content,)
        if state:
            state, message = get_top_messages(user_id, chat_id, security_level, password,)
            emit('return_message_submission', message)
            return
        emit('error_message_submission', message)
        return
    
    def on_check_filename(self, filename):
        try:
            filename = filename.split('/')[-1]
            granted_level = predict_class_level(filename)
            levels = ["Open", "Sensitive", "Top Secret"]
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
        levels = ["Open", "Sensitive", "Top Secret"]
        count = 0
        for level in levels:
            if granted_level == level:
                levels = levels[count:]
                break
            count += 1
        if file_security in levels:
            if password == False:
                password = 'False'
                encrypted_password = 'False'
            if file_security != "Open":
                file_password = filename[:1].upper() + filename[-1:].upper() + str(uuid.uuid4().int)[:4]
            status, _ = save_message(user_id, chat_id, security_level, password, False, True, filename, file_security, encrypted_password)
            if status:
                url = get_signed_url(filename)
                print(url, password)
                emit('return_file_upload', {"url":url, "password":file_password})
                emit('queue_file', {"user_id":user_id, "password":password, "filename":filename, "file_security":file_security}, namespace="filescan")
                return
            else:
                emit('error_file_upload', 'Error in handling message')
                return
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
            return
        encrypted_password = sha256_hash_bytes(chat_id+file_password+password)
        if encrypted_password == file_password_hash:
            file = return_file(chat_id, password, file_security, filename)
            emit('return_request_file', file)
            return
        else:
            emit('error_request_file', "Incorrect password")
            return
        
    def on_reflect_all_chats(self, data):
        status, message = reflect_all_chats(data.get("userId"), data.get("password"))
        if status:
            emit('return_all_chats', message)
            return
        else:
            emit('error_all_chats', message)
            return