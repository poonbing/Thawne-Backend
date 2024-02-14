from flask_socketio import Namespace, emit
from authenticate.utils import login_check, logout, verify_chat_user
import json
from utils.cryptography import encrypt_data

class AuthenticateNamespace(Namespace):
    def on_login(self, data):
        print(data)
        user_id = None
        password = None
        if "username" in data and "password" in data:
            user_id = data["username"]
            password = data["password"]
        status, message = login_check(user_id, password)
        if status:
            response = {"token": user_id}
            emit('return_login', response)
            return
        else:
            print(f"login failed: {message}")
            emit("error_login", {"error": message})
            return

    def on_logout(self, data):
        if "username" in data and "password" in data:
            user_id = data["username"]
            password = data["password"]
        logout(user_id, password)

    def on_verify_chat_user(self, data):
        print(data)
        user_id = data.get("uid")
        chat_id = data.get("cid")
        security_level = data.get("seclvl")
        password = data.get("pass")
        state, message = verify_chat_user(
            user_id,
            chat_id,
            security_level,
            password,
        )
        if state:
            print(message)
            emit("return_chat_user", message)
            return
        emit("error_chat_user", message)
        return
