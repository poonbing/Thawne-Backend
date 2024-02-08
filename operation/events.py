from flask_socketio import Namespace, emit
from .utils import create_chat, delete_chat
import json
from utils.cryptography import encrypt_data

class OperationNamespace(Namespace):
    def on_create_chat(self, data):
        print(data)
        userId = data.get("userId")
        chatName = data.get("chatName")
        chatDescription = data.get("chatDescription")
        securityLevel = data.get("securityLevel")
        listOfUsers = data.get("listOfUsers")
        generalRead = data.get("generalRead")
        generalWrite = data.get("generalWrite")
        userPassword = data.get("userPassword")
        try:
            status, message = create_chat(user_id=userId, chat_name=chatName, chat_description=chatDescription, security_level=securityLevel, list_of_users=listOfUsers, general_read=generalRead, general_write=generalWrite, password=userPassword)
            # message = encrypt_data(json.dumps(message))
            if status:
                print(message)
                emit('return_chat_creation', message)
            else:
                emit('error_chat_creation', message)
        except Exception as e:
            emit('error_chat_creation', str(e))

    
    def on_delete_chat(data):
        status, message = delete_chat(data.get("userId"), data.get("password"), data.get("chatId"))
        # message = encrypt_data(json.dumps(message))
        if status:
            emit('return_delete_chat', message)
        else:
            emit('error_delete_chat', message)
