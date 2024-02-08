from flask_socketio import Namespace, emit
from utils.data_class_model import *
from .utils import auth, db, get_top_messages, text_scanning, save_message, return_file, reflect_all_chats, get_signed_url
from utils.cryptography import generate_key, sha256_hash_bytes
import uuid
from threading import Thread








class ChatNamespace(Namespace):
    def __init__(self, namespace='/'):
        super().__init__(namespace)
        self.active_streams = {}
        
      

    class StreamHandler(Thread):
        def __init__(self, user_id, chat_id, security_level, password):
            super().__init__()
            self.user_id = user_id
            self.chat_id = chat_id
            self.security_level = security_level
            self.password = password
            self.user = auth.sign_in_with_email_and_password(chat_id.lower() + "@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
            self.stream = db.child("chats").child(chat_id).child(security_level).child("chat_history").stream(lambda x: self.stream_update(), stream_id=user_id, token=self.user["idToken"])

        def stream_update(self):
            status, message = get_top_messages(self.user_id, self.chat_id, self.security_level, self.password)
            if status:
                emit('return_message_list', message)
            else:
                emit('error_message_list', message)

        def run(self):
            self.stream.start()

        def stop(self):
            self.stream.close()

    def on_get_message_list(self, data):
        user_id = data.get("userId")
        chat_id = data.get("chatId")
        security_level = data.get("securityLevel")
        password = data.get("pass")
        if password == False:
            password = 'false'
        state, message = get_top_messages(user_id, chat_id, security_level, password,)
        if state:
            stream_handler = self.StreamHandler(user_id, chat_id, security_level, password)
            stream_handler.start()
            self.active_streams[user_id] = stream_handler
            emit('return_message_list', message)
        else:
            emit('error_message_list', message)

    def on_submit_message(self, data):
        print(data)
        user_id = data.get("userId")
        chat_id = data.get("chatId")
        security_level = data.get("securityLevel")
        password = data.get("chatPassword")
        message_content = data.get("message")
        if password == False:
            password = 'false'
        try:
            filename = data.get("filename")
            file_security = data.get("file security")
            state, message = save_message(user_id, chat_id, security_level, password, message_content, True, filename, file_security,)
        except:
            state, message = save_message(user_id, chat_id, security_level, password, message_content)
            print(state)
            print(message)
        if state:
            state, message = get_top_messages(user_id, chat_id, security_level, password,)
            emit('return_message_submission', message)
        else:
            emit('error_message_submission', message)
    
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
            print(status)
            if status:
                emit('return_file_upload', {"url":url, "password":file_password})
                emit('queue_file', {"user_id":user_id, "password":password, "filename":filename, "file_security":file_security}, namespace="filescan")
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
            if user_id in self.active_streams:
                stream_handler = self.active_streams.pop(user_id)
                stream_handler.stop()
            emit('return_all_chats', message)
        else:
            emit('error_all_chats', message)


