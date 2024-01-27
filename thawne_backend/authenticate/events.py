from flask_socketio import Namespace, emit
from .utils import login_check, verify_chat_user


class AuthenticateNamespace(Namespace):
    def on_login(self, data):
        print('Received login request: ', data)
        user_id = None
        password = None
        if "username" in data and "password" in data:
            user_id = data["username"]
            password = data["password"]
        result, message = login_check(user_id, password)
        if result:
            emit('return_login', {"token": user_id})
            return
        else:
            emit('error_login', {"error": message})
            return

    def on_verify_chat_user(self, data):
        user_id = data.get("uid")
        chat_id = data.get("cid")
        security_level = data.get("seclvl")
        password = data.get("pass")
        state, message = verify_chat_user(user_id, chat_id, security_level, password,)
        if state:
            emit('return_chat_user', message)
            return
        emit('error_chat_user', message)
        return