from flask_socketio import Namespace, emit
from .utils import create_chat

class OperationNamespace(Namespace):
    def on_create_chat(data):
        userId = data.get("userId")
        chatName = data.get("chatName")
        chatDescription = data.get("chatDescription")
        securityLevel = data.get("securityLevel")
        listOfUsers = data.get("listOfUsers")
        generalRead = data.get("generalRead")
        generalWrite = data.get("generalWrite")
        status, message = create_chat(user_id=userId, chat_name=chatName, chat_description=chatDescription, security_level=securityLevel, list_of_users=listOfUsers, general_read=generalRead, general_write=generalWrite,)
        if status:
            emit('return_chat_creation', message)
            return
        emit('error_chat_creation', message)
        return