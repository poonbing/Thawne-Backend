from datetime import datetime
import uuid
import bcrypt
from cryptography import *
from app import db, storage


def login_check(user_id, password):
    try:
        user_data = db.child("users").child(user_id).get().val()
        if user_data:
            stored_key = user_data.get("key", "")
            salt = bytes(user_data.get("user_id", "")[8:], encoding="utf-8")
            if stored_key == str(
                bcrypt.hashpw(password.encode("utf-8"), salt), encoding="utf-8"
            ):
                if user_data.get("status") == "Enabled":
                    return True, user_data.get("chats", {})
                elif user_data.get("status") == "Disabled":
                    return False, "User has been Disabled."
            else:
                return False, "Incorrect Username or Password."
        else:
            return False, "User does not exist."
    except Exception as e:
        return False, f"Error during login check: {str(e)}"


def verify_chat_user(user_id, chat_id, security_level, password):
    try:
        chat = (
            db.child("chats")
            .child(chat_id)
            .child(security_level)
            .child(password)
        )
        if not chat:
            return False, "Incorrect chat information."
        member_list = chat.get().val()["members"]
        if user_id in member_list:
            return True, member_list
        else:
            return False, "User not in the chat group."
    except Exception as e:
        return False, f"Error verifying chat user: {str(e)}"


def check_user_access(user_id, chat_id):
    user_access = (
        db.child("users")
        .child(user_id)
        .child("chats")
        .child(chat_id)
        .get()
        .val()["access"]
    )
    return user_access or {"read": False, "write": False}


def get_top_messages(user_id, chat_id, security_level, password, message_count=20):
    check, status = verify_chat_user(user_id, chat_id, security_level, password)
    if not check:
        return False, status
    access = check_user_access(user_id, chat_id)
    if not access["read"]:
        return False, "User does not have permission to access this chat."
    chat = db.child("chats").child(chat_id).child(security_level).child(password)
    messages = chat.get().val()["chat_history"]
    message_list = list(reversed(messages.values()))
    if password != "":
        for message_data in message_list:
            message_data["content"] = decrypt_data(message_data["content"], password)
    return True, message_list


def save_message(
    user_id,
    chat_id,
    security_level,
    password,
    message_content,
    file=False,
    filename=False,
    file_security=False,
):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    check, status = verify_chat_user(user_id, chat_id, security_level, password)
    if not check:
        return False, status
    access = check_user_access(user_id, chat_id)
    if not access["write"]:
        return False, "User does not have permission to send messages in this chat."
    try:
        user = db.child("users").child(user_id).get().val()
        new_message_count = str(
            int(
                db.child("chats")
                .child(chat_id)
                .child(security_level)
                .child(password)
                .child("message_count")
                .get()
                .val()
            )
            + 1
        ).zfill(6)
        new_message_id = f"{chat_id}{new_message_count}"
        print(new_message_id)
        if password:
            print(password)
            message_content = encrypt_data(message_content, password)
        new_message = {
            "id": new_message_id,
            "date": timestamp,
            "sent_from": {user_id: user["username"]},
            "content": message_content,
        }
        if file:
            new_message["file"] = {
                "filename": filename,
                "file_url": storage.child(filename).get_url(None),
                "file_security": file_security,
            }
            if file_security in ["Top Secret", "Sensitive"]:
                file_pass = str(uuid.uuid4())[:8]
                salt = generate_salt()
                key = str(
                    bcrypt.hashpw(file_pass.encode("utf-8"), salt), encoding="utf-8"
                )
                new_message["file"]["file_password"] = key
                storage.child(filename).put(file)
        message_list = db.child("chats").child(chat_id).child(security_level).child(password).child("chat_history").get().val()
        if message_list != None:
            message_list[new_message_count] = new_message
        else:
            message_list = {new_message_count:new_message}
        members_list = db.child("chats").child(chat_id).child(security_level).child(password).child("members").get().val()
        db.child("chats").child(chat_id).child(security_level).child(
            password
        ).set({"chat_history":message_list, "members":members_list})
        db.child("chats").child(chat_id).child(security_level).child(
            password
        ).update({"message_count":int(new_message_count), })
        if file:
            return True, {new_message_id: {filename: file_pass}}
        else:
            return True, new_message_id
    except Exception as e:
        print(e)
        return False, "Error in message saving."


def augment_user(user_id, subject_user_id, keyword):
    valid_keywords = ["Enabled", "Disabled"]
    if keyword not in valid_keywords:
        return False, f"Invalid keyword: {keyword}"
    user_level = db.child("users").child(user_id).child("level").get().val()
    subject_user_level = (
        db.child("users").child(subject_user_id).child("level").get().val()
    )
    if user_level != "master":
        return False, f"You do not have permissions to apply {keyword} to accounts."
    if subject_user_level == user_level:
        return (
            False,
            f"{subject_user_id} is at the same privilege level and cannot be {keyword}.",
        )
    #print(db.child("users").child(subject_user_id).get().val()["status"])
    db.child("users").child(subject_user_id).update({"status":keyword})
    return True, f"{subject_user_id} has been {keyword}."


def augment_user_chat_permission(user_id, subject_user_id, chat_id, keyword, status):
    valid_keywords = ["read", "write"]
    if keyword not in valid_keywords:
        return False, f"Invalid keyword: {keyword}"
    user_level = db.child("users").child(user_id).child("level").get().val()
    subject_user_level = (
        db.child("users").child(subject_user_id).child("level").get().val()
    )
    if user_level != "master":
        return (
            False,
            f"You do not have permissions to alter {keyword} permission of accounts.",
        )
    if subject_user_level == user_level:
        return (
            False,
            f"{subject_user_id} is at the same privilege level and cannot be altered.",
        )
    db.child("users").child(subject_user_id).child("chats").child(chat_id).child(
        "access"
    ).update({keyword:status})
    return (
        True,
        f"{subject_user_id}'s {keyword} permission for {chat_id} has been changed to {status}.",
    )


def create_chat(
    user_id,
    chat_name,
    chat_description,
    security_level,
    list_of_users,
    general_read=True,
    general_write=True,
):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    chat_id = str(uuid.uuid4())[:12]
    user_level = db.child("users").child(user_id).child("level").get().val()
    if user_level not in ["admin", "master"]:
        return False, "User does not have permissions to create chats."
    if security_level == "Open":
        password = False
    elif security_level in ["Sensitive", "Top Secret"] and user_level == "admin":
        return (
            False,
            "User does not have permissions to create Sensitive or Top Secret chats.",
        )
    else:
        password = str(uuid.uuid4())[:12]
    creator = db.child("users").child(user_id).get().val()["username"]
    list_of_users.append(user_id)
    chat_data = {
        chat_id: {
            security_level: {
                password: {
                    "members": list_of_users,
                    "chat_history": {},
                    "message_count": 0,
                },
            },
            "chat_name": chat_name,
            "creation_date": timestamp,
            "chat_description": chat_description,
            "creator": creator,
        }
    }
    db.child("chats").update(chat_data)
    for user in list_of_users:
        user_chats = db.child("users").child(user).child("chats").get().val() or {}
        user_chats[chat_id] = {
            "security level": security_level,
            "access": {"read": general_read, "write": general_write},
        }
        db.child("users").child(user).child("chats").update(user_chats)
    if security_level == "Open":
        return f"{chat_id} has been created by {creator}. The security level is {security_level}."
    else:
        return f"{chat_id} has been created by {creator}. The security level is {security_level}. The following is the password: {password}"


def mass_user_creation(user_data):
    result = []
    for name, data in user_data.items():
        user_id = str(uuid.uuid4())[:8]
        salt = generate_salt()
        password = data["password"]
        key = str(bcrypt.hashpw(password.encode("utf-8"), salt), encoding="utf-8")
        entry = {
            "user_id": user_id + str(salt, encoding="utf-8"),
            "username": name,
            "key": key,
            "email": data["email"],
            "level": data["level"],
            "status": "Enabled",
            "chats": {},
        }
        db.child("users").child(name).update(entry)
        result.append({name: {user_id: password}})
    return True, result


def reflect_all_chats(user_id):
    return_list = []
    user_chats = db.child("users").child(user_id).child("chats").get().val()
    chats = db.child("chats").get().val()
    if user_chats and chats:
        for chat_id in user_chats:
            chat_dict = {}
            chat_name = chats[chat_id]["chat_name"]
            chat_level = user_chats[chat_id]["security level"]
            chat_dict["chat_id"] = chat_id
            chat_dict["chat_name"] = chat_name
            chat_dict["security_level"] = chat_level
            return_list.append(chat_dict)
        print(return_list)
        return return_list
    else:
        return False, "Error in retrieving chats"


def remove_user_from_chat(user_id, chat_id, security_level, password, removed_user_id):
    user_levels = {"master": 1, "admin": 2, "user": 3}
    user_level = db.child("users").child(user_id).child("level").get().val()
    target_user_level = (
        db.child("users").child(removed_user_id).child("level").get().val()
    )
    if user_levels.get(user_level, 0) < user_levels.get(target_user_level, 0):
        return False, "User does not have permission to remove users."
    chat_members = (
        db.child("chats")
        .child(chat_id)
        .child(security_level)
        .child(password)
        .child("members")
        .get()
        .val()
    )
    chat_members = {
        item: user_id
        for item, member_id in chat_members.items()
        if member_id != removed_user_id
    }
    db.child("chats").child(chat_id).child(security_level).child(password).child(
        "members"
    ).set(chat_members)
    target_chats = (
        db.child("users").child(removed_user_id).child("chats").get().val() or {}
    )
    target_chats.pop(chat_id, None)
    db.child("users").child(removed_user_id).child("chats").set(target_chats)
    return True, "User is removed from the chat successfully."


def delete_chat(user_id, chat_id, security_level, password):
    target_chat = db.child("chats").child(chat_id).child(security_level).get().val()
    if not target_chat or not target_chat.get(password):
        return False, "Invalid chat or password."
    user_level = db.child("users").child(user_id).child("level").get().val()
    if target_chat["creator"] != user_id and user_level != "master":
        return False, "User cannot delete the chat."
    member_list = target_chat.get(password, {}).get("members", [])
    for member_id in member_list:
        db.child("users").child(member_id).child("chats").child(chat_id).remove()
    db.child("chats").child(chat_id).remove()
    return True, "Chat has been deleted successfully"


def delete_user(user_id, removed_user_id):
    user_level = db.child("users").child(user_id).child("level").get().val()
    target_user = db.child("users").child(removed_user_id).get().val()
    if not target_user:
        return False, "Invalid user."
    if user_level == "master":
        db.child("users").child(removed_user_id).remove()
        for chat_id, chat_info in target_user.get("chats", {}).items():
            security_level = chat_info.get("security level", "")
            for chat_password in (
                db.child("chats").child(chat_id).child(security_level).get().val() or {}
            ):
                member_list = (
                    db.child("chats")
                    .child(chat_id)
                    .child(security_level)
                    .child(chat_password)
                    .child("members")
                    .get()
                    .val()
                    or {}
                )
                member_list = {
                    uid: uname
                    for uid, uname in member_list.items()
                    if uid != removed_user_id
                }
                db.child("chats").child(chat_id).child(security_level).child(
                    chat_password
                ).child("members").set(member_list)
        return True, "User has been deleted successfully."
    elif user_level == target_user.get("level"):
        return False, "User cannot delete another user of the same permission level."
    else:
        return False, "User does not have permission to delete users."


def obtain_chat_details(chat_id, security_level, password):
    member_list = (
        db.child("chats")
        .child(chat_id)
        .child(security_level)
        .child(password)
        .child("members")
        .get()
        .val()
        or {}
    )
    members = {}
    for user_id, role in member_list.items():
        username = db.child("users").child(user_id).child("username").get().val()
        members[username] = "Member"
    chat_info = db.child("chats").child(chat_id).child(security_level).get().val() or {}
    creator_username = (
        db.child("users")
        .child(chat_info.get("creator", ""))
        .child("username")
        .get()
        .val()
    )
    members[creator_username] = "Creator"
    return_dict = {
        "chat_name": chat_info.get("chat_name", ""),
        "chat_description": chat_info.get("chat_description", ""),
        "creation_date": chat_info.get("creation_date", ""),
        "members": members,
    }
    return True, return_dict
