from datetime import datetime
import uuid
import bcrypt
from cryptography import *
from app import db

def login_check(user_id, password):
    try:
        user_data = db.child('users').child(user_id).get().val()
        salt = user_data["user_id"][8:]
        if user_data and user_data["key"] == bcrypt.hashpw(password.encode('utf-8'), salt):
            if user_data["status"] == "Enabled":
                return True, user_data.get('chats', {})
            elif user_data["status"] == "Disabled":
                return False, "User has been Disabled."
        else:
            return False, "Incorrect Password."
    except:
        return False, "User does not exist."

def verify_chat_user(user_id, chat_id, security_level, password):
    try:
        chat = db.child('chats').child(chat_id).child(security_level).child(password)
        member_list = chat.child("members").get().val()
        if user_id in member_list:
            return True, chat
        else:
            return False, "User not in chat group."
    except:
        return False, "Incorrect chat information."

def check_user_access(user_id, chat_id):
    user_access = db.child("users").child(user_id).child("chats").child(chat_id).child("access").get().val()
    return user_access

def get_top_messages(user_id, chat_id, security_level, password, message_count):
    check, status = verify_chat_user(user_id, chat_id, security_level, password)
    if check:
        access = check_user_access(user_id, chat_id)
        if access["read"]:
            try:
                messages = status.child("chat_history").limit_to_last(message_count).get().val()
            except:
                messages = status.child("chat_history").get().val()
            message_list = list(reversed(messages))
            if password != "":
                for message_id in message_list:
                    message_list[message_id]["content"] = decrypt_data(message_list[message_id]["content"], password)
            return True, message_list
        else:
            return False, "User does not have permission to access this chat."
    else:
        return False, status

def save_message(user_id, chat_id, security_level, password, message_content):
    timestamp = int(datetime.utcnow().timestamp()*1000)
    check, status = verify_chat_user(user_id, chat_id, security_level, password)
    if check:
        access = check_user_access(user_id, chat_id)
        if access["write"]:
            new_message_count = str(int(status.child("message_count").get().val())+1).zfill(6)
            new_message_id = chat_id+new_message_count
            if password != "":
                message_content = encrypt_data(message_content, password)
            new_message = {
                "id":new_message_id,
                "date":timestamp,
                "sent_from":user_id,
                "content":message_content
            }
            try:
                db.child('chats').child(chat_id).child(security_level).child(password).child("chat_history").push(new_message)
                db.child('chats').child(chat_id).child(security_level).child(password).child("message_count").update(new_message_count)
                return True, new_message_id
            except:
                return False, "Error in message saving."
        else:
            return False, "User does not have permission to send messages in this chat."
    else:
        return False, status

def get_all_chat(user_id):
    chat_list = db.child("users").child(user_id).child("chats").get().val()
    return chat_list

def augment_user(user_id, subject_user_id, keyword):
    if keyword in ["Enabled", "Disabled"]:
        user_level = db.child("users").child(user_id).child("level").get().val()
        if user_level == "admin":
            subject_user_level = db.child("users").child(subject_user_id).child("level").get().val()
            if subject_user_level != user_level:
                db.child("users").child(subject_user_id).child("status").update(keyword)
                return True, f"{subject_user_id} has been {keyword}."
            else:
                return False, f"{subject_user_id} is at the same priviledge level, thus cannot be {keyword}."
        else:
            return False, f"You do not have permissions to apply {keyword} to accounts."
        
def augment_user_chat_permission(user_id, subject_user_id, chat_id, keyword, status):
    if keyword in ["read", "write"]:
        user_level = db.child("users").child(user_id).child("level").get().val()
        if user_level == "admin":
            subject_user_level = db.child("users").child(subject_user_id).child("level").get().val()
            if subject_user_level != user_level:
                db.child("users").child(subject_user_id).child("chats").child(chat_id).child("access").child(keyword).update(status)
                return True, f"{subject_user_id}'s {keyword} permission to {chat_id} has been changed to {status}."
            else:
                return False, f"{subject_user_id} is at the same priviledge level, thus cannot be altered."
        else:
            return False, f"You do not have permissions to alter {keyword} permission of accounts."
    
def create_chat(user_id, chat_name, chat_description, chat_id, security_level, list_of_users, general_read, general_write):
    timestamp = int(datetime.utcnow().timestamp()*1000)
    user_level = db.child("users").child(user_id).child("level").get().val()
    # if user_level == "admin":
    if security_level == "Open":
        password = ""
    else:
        password = str(uuid.uuid4())[:12]
    db.child("chats").update(
        {chat_id:{security_level:{password:{"members": list_of_users,"chat_history": {},"message_count":0},}},"chat_name":chat_name, "creation_date":timestamp, "chat_description":chat_description})
    for user_id in list_of_users:
        chats = db.child("users").child(user_id).child("chats").get().val()
        chats[chat_id] = {"security level":security_level, "access":{"read":general_read, "write":general_write}}
        db.child("users").child(user_id).child("chats").update(chats)
    if security_level == "Open":
        return True, f"{chat_id} has been created. The security level is {security_level}."
    else:
        return True, f"{chat_id} has been created. The security level is {security_level}. The following is the password: {password}"
    # else:
    #     return False, "User does not have permissions to create chats."

def mass_user_creation(dictionary):
    result = {"username":{"user id":"password"}}
    for name in dictionary:
        user_id = str(uuid.uuid4())[:8]
        salt = generate_salt()
        password = dictionary[name]["password"]
        key = bcrypt.hashpw(password.encode('utf-8'), salt)
        entry = {
            "user_id":user_id+salt,
            "username":name,
            "key":key,
            "email":dictionary[name]["email"],
            "level":dictionary[name]["level"],
            "status":"Enabled",
            "chats":{}
        }
        db.child("users").child(name).update(entry)
        result[name] = {user_id:password}
    return True, result



