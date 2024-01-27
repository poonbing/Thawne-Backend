from datetime import datetime
import uuid, re
import bcrypt
from cryptography import *
from app import db, storage, auth


sensitive_data = [
    r'^[SFTG]\d{7}[A-Z]$', #NRIC
    r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$',  #IPv4
    r'^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$',  #Mastercard
    r'\b([4]\d{3}[\s]\d{4}[\s]\d{4}[\s]\d{4}|[4]\d{3}[-]\d{4}[-]\d{4}[-]\d{4}|[4]\d{3}[.]\d{4}[.]\d{4}[.]\d{4}|[4]\d{3}\d{4}\d{4}\d{4})\b', #Visa
    r'^3[47][0-9]{13}$',  #Amex
    r'\b[\w.-]{0,25}@(yahoo|hotmail|gmail)\.com\b' #Email
]

def text_scanning(text):
    sensitive_data = [
    r'^[SFTG]\d{7}[A-Z]$', #NRIC
    r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$',  #IPv4
    r'^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$',  #Mastercard
    r'\b([4]\d{3}[\s]\d{4}[\s]\d{4}[\s]\d{4}|[4]\d{3}[-]\d{4}[-]\d{4}[-]\d{4}|[4]\d{3}[.]\d{4}[.]\d{4}[.]\d{4}|[4]\d{3}\d{4}\d{4}\d{4})\b', #Visa
    r'^3[47][0-9]{13}$',  #Amex
    r'\b[\w.-]{0,25}@(yahoo|hotmail|gmail)\.com\b' #Email
    ]
    words = text.split()  # Split the sentence into words
    for word in words:
        for pattern in sensitive_data:
            search = re.search(pattern, word, re.IGNORECASE)
            if search:
                matched_word = search.group()
                print('Matched:', matched_word)
                return matched_word

def login_check(user_id, password):
    try:
        user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
        print(f"local user id = {user['localId']}")
        user_data = db.child("users").child(user['localId']).get(token=user['idToken']).val()
        print(user_data)
        if user_data:
            if user_data["status"] == 'Enabled':
                try:
                    return True, user_data["chats"]
                except:
                    return True, "No chats available."
            elif user_data["status"] == 'Disabled':
                return False, f"User account disabled."
        else:
            return False, "Incorrect Username or Password."
    except Exception as e:
        return False, f"Error during login check: {str(e)}"


def verify_chat_user(user_id, chat_id, security_level, password):
    try:
        chat = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
        if not chat:
            return False, "Incorrect chat information."
        member_list = db.child("chats").child(chat_id).child(security_level).child("members").get(token=chat['idToken']).val()
        if user_id in member_list:
            return True, {user_id:member_list[user_id]}
        else:
            return False, "User not in the chat group."
    except Exception as e:
        return False, f"Error verifying chat user: {str(e)}"


# def check_user_access(user_id, chat_id):
#     user_access = (
#         db.child("users")
#         .child(user_id)
#         .child("chats")
#         .child(chat_id)
#         .get()
#         .val()["access"]
#     )
#     return user_access or {"read": False, "write": False}


def get_top_messages(user_id, chat_id, security_level, password):
    check, status = verify_chat_user(user_id, chat_id, security_level, password)
    if not check:
            return False, status
    try:
        chat = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
        message_list = db.child("chats").child(chat_id).child(security_level).child("chat_history").get(token=chat['idToken']).val()
        if password != 'false':
            for message_data in message_list:
                message_data["content"] = decrypt_data(message_data["content"], password)
        return True, message_list
    except:
        return True, "Chat does not have messages yet."


def save_message(user_id, chat_id, security_level, password, message_content, file=False, filename=False, file_security=False, file_password=False):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    check, status = verify_chat_user(user_id, chat_id, security_level, password)
    if not check:
        return False, status
    try:
        chat = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
        chat_info = db.child("chats").child(chat_id).child(security_level).get(token=chat['idToken']).val()
        new_message_count = str(int(chat_info["message_count"]) + 1).zfill(6)
        new_message_id = f"{chat_id}{new_message_count}"
        new_message = {
            "id": new_message_id,
            "date": timestamp,
            "sent_from": {user_id: status[user_id]},
        }
        if message_content:
            if password != 'false':
                message_content = encrypt_data(message_content, password)
            new_message['content'] = message_content
        if file:
            new_message["content"] = {
                "filename": filename,
                "file_security": file_security,
                "file_password": file_password
            }
        try:
            message_list = chat_info["chat_history"]
            message_list[new_message_count] = new_message
        except:
            message_list = {new_message_count:new_message}
        db.child("chats").child(chat_id).child(security_level).child("chat_history").set(message_list, token=chat['idToken'])
        db.child("chats").child(chat_id).child(security_level).child("message_count").set(new_message_count, token=chat['idToken'])
        return True, new_message_id
    except Exception as e:
        return False, f"Error in message saving.{e}"

def store_file(chat_id, password, filename, file, file_security):
    user = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
    if not user:
        return False, "Incorrect User information."
    try:
        storage.child(f'files/{chat_id}/{file_security}/{filename}').put(file, user['idToken'])
        return True, "File upload successful."
    except:
        return False, "Error in file upload."

# def augment_user(user_id, subject_user_id, keyword):
#     valid_keywords = ["Enabled", "Disabled"]
#     if keyword not in valid_keywords:
#         return False, f"Invalid keyword: {keyword}"
#     user_level = db.child("users").child(user_id).child("level").get().val()
#     subject_user_level = (
#         db.child("users").child(subject_user_id).child("level").get().val()
#     )
#     if user_level != "master":
#         return False, f"You do not have permissions to apply {keyword} to accounts."
#     if subject_user_level == user_level:
#         return (
#             False,
#             f"{subject_user_id} is at the same privilege level and cannot be {keyword}.",
#         )
#     #print(db.child("users").child(subject_user_id).get().val()["status"])
#     db.child("users").child(subject_user_id).update({"status":keyword})
#     return True, f"{subject_user_id} has been {keyword}."


# def augment_user_chat_permission(user_id, subject_user_id, chat_id, keyword, status):
#     valid_keywords = ["read", "write"]
#     if keyword not in valid_keywords:
#         return False, f"Invalid keyword: {keyword}"
#     user_level = db.child("users").child(user_id).child("level").get().val()
#     subject_user_level = (
#         db.child("users").child(subject_user_id).child("level").get().val()
#     )
#     if user_level != "master":
#         return (
#             False,
#             f"You do not have permissions to alter {keyword} permission of accounts.",
#         )
#     if subject_user_level == user_level:
#         return (
#             False,
#             f"{subject_user_id} is at the same privilege level and cannot be altered.",
#         )
#     db.child("users").child(subject_user_id).child("chats").child(chat_id).child(
#         "access"
#     ).update({keyword:status})
#     return (
#         True,
#         f"{subject_user_id}'s {keyword} permission for {chat_id} has been changed to {status}.",
#     )


def create_chat(user_id, password, chat_name, chat_description, security_level, list_of_users, general_read=True, general_write=True,):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    chat_id = security_level[:1].upper() + str(uuid.uuid4().int)[:6] + security_level[-1:].upper()
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    user_info = db.child("users").child(user['localId']).get(token=user['idToken']).val()
    user_level = user_info["level"]
    if user_level not in ["admin", "master"]:
        return False, "User does not have permissions to create chats."
    if security_level == "Open":
        password = 'false'
    elif security_level in ["Sensitive", "Top Secret"] and user_level == "admin":
        return False, "User does not have permissions to create Sensitive or Top Secret chats.",
    else:
        password = security_level[:1].upper() + security_level[-1:].upper() + str(uuid.uuid4().int)[:4] 
    creator = user_info["username"]
    list_of_users[user_id] = creator
    chat_data = {
        chat_id: {
            security_level:{
                    "chat_history":{},
                    "members": list_of_users,
                    "member_count": len(list_of_users),
                    "message_count": 0,
                },
            "chat_name": chat_name,
            "creation_date": timestamp,
            "chat_description": chat_description,
            "creator": creator,
        }
    }
    db.child("chats").update(chat_data, token=user['idToken'])
    auth.create_user_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
    users = db.child("users").get(token=user['idToken']).val()
    for uid in users:
        name = users[uid]["username"]
        if name in list_of_users.values():
            try:
                users[uid]["chats"][chat_id] = {"chat_name":chat_name,
                                                "security_level": security_level,
                                                "access": {"read": general_read,
                                                        "write": general_write},}
            except:
                users[uid]["chats"] = {chat_id:{"chat_name":chat_name,
                                                "security_level": security_level,
                                                "access": {"read": general_read,
                                                        "write": general_write},}}
    db.child("users").set(users, token=user['idToken'])
    if security_level == "Open":
        return True, f"{chat_id} has been created by {creator}. The security level is {security_level}."
    else:
        return True, f"{chat_id} has been created by {creator}. The security level is {security_level}. The following is the password: {password}"


def mass_user_creation(user_data):
    result = []
    for name, data in user_data.items():
        user_id = ("u"+str(data["level"][:1])).upper()+str(uuid.uuid4().int)[:5]
        password = data["password"]
        key = generate_key(user_id.lower(), password.lower())
        auth.create_user_with_email_and_password(user_id.lower()+"@thawne.com", key[:20])
        entry = {
            "user_id": user_id,
            "username": name,
            "email": data["email"],
            "level": data["level"],
            "status": "Enabled",
            "chats": {},
        }
        user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", key[:20])
        db.child("users").child(user['localId']).update(entry, token=user['idToken'])
        result.append({name: {user_id: password}})
    return True, result


def reflect_all_chats(user_id, password):
    return_list = []
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    user_chats = db.child("users").child(user['localId']).child("chats").get(token=user['idToken']).val()
    if user_chats:
        for chat_id in user_chats:
            chat_dict = {}
            chat_dict["chat_id"] = chat_id
            chat_dict["chat_name"] = user_chats[chat_id]["chat_name"]
            chat_dict["security_level"] = user_chats[chat_id]["security_level"]
            return_list.append(chat_dict)
        return True, return_list
    else:
        return False, "Error in retrieving chats"


# def remove_user_from_chat(user_id, chat_id, security_level, password, removed_user_id):
#     user_level = db.child("users").child(user_id).child("level").get().val()
#     target_user_level = (
#         db.child("users").child(removed_user_id).child("level").get().val()
#     )
#     if user_level != "master" and target_user_level != "master":
#         return False, "User does not have permission to remove users."
#     chat_members = (
#         db.child("chats")
#         .child(chat_id)
#         .child(security_level)
#         .child(password)
#         .get()
#         .val()
#         ["members"]
#     )
#     chat_members.remove(removed_user_id)
#     db.child("chats").child(chat_id).child(security_level).child(password).update({"members":chat_members})
#     target_chats = (
#         db.child("users").child(removed_user_id).child("chats").get().val() or {}
#     )
#     target_chats.pop(chat_id, None)
#     db.child("users").child(removed_user_id).child("chats").set(target_chats)
#     return True, "User is removed from the chat successfully."


# def add_user_to_chat(user_id, chat_id, security_level, password, new_user_id):
#     user_level = db.child("users").child(user_id).child("level").get().val()
#     if user_level != "master":
#         return False, "User does not have permission to add users."
#     chat_members = (
#         db.child("chats")
#         .child(chat_id)
#         .child(security_level)
#         .child(password)
#         .get()
#         .val()
#         ["members"]
#     )
#     chat_members.append(new_user_id)
#     db.child("chats").child(chat_id).child(security_level).child(password).update({"members":chat_members})
#     target_chats = (
#         db.child("users").child(new_user_id).child("chats").get().val() or {}
#     )
#     target_chats[chat_id] = {"access":{"read":True, "write":True}, "security level":security_level}
#     db.child("users").child(new_user_id).child("chats").update(target_chats)
#     return True, "User is removed from the chat successfully."


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


# def delete_user(user_id, removed_user_id):
#     user_level = db.child("users").child(user_id).child("level").get().val()
#     target_user = db.child("users").child(removed_user_id).get().val()
#     if not target_user:
#         return False, "Invalid user."
#     if user_level == "master":
#         db.child("users").child(removed_user_id).remove()
#         for chat_id, chat_info in target_user.get("chats", {}).items():
#             security_level = chat_info.get("security level", "")
#             for chat_password in (
#                 db.child("chats").child(chat_id).child(security_level).get().val() or {}
#             ):
#                 member_list = (
#                     db.child("chats")
#                     .child(chat_id)
#                     .child(security_level)
#                     .child(chat_password)
#                     .child("members")
#                     .get()
#                     .val()
#                     or {}
#                 )
#                 member_list = {
#                     uid: uname
#                     for uid, uname in member_list.items()
#                     if uid != removed_user_id
#                 }
#                 db.child("chats").child(chat_id).child(security_level).child(
#                     chat_password
#                 ).child("members").set(member_list)
#         return True, "User has been deleted successfully."
#     elif user_level == target_user.get("level"):
#         return False, "User cannot delete another user of the same permission level."
#     else:
#         return False, "User does not have permission to delete users."


# def obtain_chat_details(chat_id, security_level, password):
#     chat = (
#         db.child("chats")
#         .child(chat_id)
#         .child(security_level)
#         .child(password)
#         .get()
#         .val()
#         or {}
#     )
#     members = {}
#     chat_info = db.child("chats").child(chat_id).get().val() or {}
#     for user_id in chat["members"]:
#         username = db.child("users").child(user_id).child("username").get().val()
#         if username == chat_info["creator"]:
#             members[username] = "Creator"
#         else:
#             members[username] = "Member"
#     return_dict = {
#         "chat_name": chat_info["chat_name"],
#         "chat_description": chat_info["chat_description"],
#         "creation_date": chat_info["creation_date"],
#         "members": members,
#     }
#     return True, return_dict

def log_event(user_id, password, type_of_offense, location, context):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    user = auth.sign_in_with_email_and_password(user_id.lower()+"@thawne.com", generate_key(user_id.lower(), password.lower())[:20])
    if not user:
        return False, "Incorrect User information, please retry."
    try:
        id_list = list(db.child("logs queue").shallow().get(user['idToken']).val())
        counter = str(int(max(id_list, key=lambda x: int(x))) + 1).zfill(6)
    except:
        counter = '000000'
    log = {type_of_offense:{timestamp:{user_id:{location:{"offense_context":context}}}}}
    try:
        db.child("logs queue").child(counter).update(log, user['idToken'])
    except:
        return False, "Error in logging"
    return True, "Log Queued"

def return_file(chat_id, password, file_security, filename):
    user = auth.sign_in_with_email_and_password(chat_id.lower()+"@thawne.com", generate_key(chat_id.lower(), password.lower())[:20])
    if not user:
        return False, "Incorrect User information."
    try:
        file = storage.child(f'files/{chat_id}/{file_security}/{filename}').download(user['idToken'])
        return True, file
    except:
        return False, "Error in obtaining file."