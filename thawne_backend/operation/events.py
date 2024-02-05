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
    
    def on_delete_chat(data):
        pass




# def delete_chat(user_id, chat_id, security_level, password):
#     target_chat = db.child("chats").child(chat_id).child(security_level).child(password).get().val()
#     if target_chat == None:
#         return False, "Invalid chat or password."
#     username = db.child("users").child(user_id).child("username").get().val()
#     if db.child("chats").child(chat_id).get().val()["creator"] != username:
#         return False, "User cannot delete the chat."
#     member_list = target_chat["members"]
#     for member_id in member_list:
#         db.child("users").child(member_id).child("chats").child(chat_id).remove()
#     db.child("chats").child(chat_id).remove()
#     return True, "Chat has been deleted successfully"