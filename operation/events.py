from flask_socketio import Namespace, emit
from .utils import create_chat, delete_chat

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
            if status:
                print(message)
                emit('return_chat_creation', message)
            else:
                emit('error_chat_creation', message)
        except Exception as e:
            emit('error_chat_creation', str(e))

    
    def on_delete_chat(data):
        status, message = delete_chat(data.get("userId"), data.get("password"), data.get("chatId"))
        if status:
            emit('return_delete_chat', message)
        else:
            emit('error_delete_chat', message)




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