import pyrebase
from datetime import datetime
import uuid
from utils.cryptography import generate_key

firebase_config = {
    "apiKey": "AIzaSyCslAm25aJkWReYOOXV8YNAGzsCVRLkxeM",
    "authDomain": "thawne-d1541.firebaseapp.com",
    "databaseURL": "https://thawne-d1541-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "thawne-d1541",
    "storageBucket": "thawne-d1541.appspot.com",
    "messagingSenderId": "101144409530",
    "appId": "1:101144409530:web:4f2663a71c5c204b4c5983",
    "measurementId": "G-N2NEVEDM49",
}


firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def create_chat(
    user_id,
    password,
    chat_name,
    chat_description,
    security_level,
    list_of_users,
    general_read=True,
    general_write=True,
):
    member_list = {}
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    chat_id = (
        security_level[:1].upper()
        + str(uuid.uuid4().int)[:6]
        + security_level[-1:].upper()
    )
    user = auth.sign_in_with_email_and_password(
        user_id.lower() + "@thawne.com",
        generate_key(user_id.lower(), password.lower())[:20],
    )
    users = db.child("users").get(token=user["idToken"]).val()
    user_info = (
        db.child("users").child(user["localId"]).get(token=user["idToken"]).val()
    )
    user_level = user_info["level"]
    if user_level not in ["admin", "master"]:
        return False, "User does not have permissions to create chats."
    if security_level == "Open":
        password = "false"
    elif security_level in ["Sensitive", "Top Secret"] and user_level == "admin":
        return (
            False,
            "User does not have permissions to create Sensitive or Top Secret chats.",
        )
    else:
        password = (
            security_level[:1].upper()
            + security_level[-1:].upper()
            + str(uuid.uuid4().int)[:4]
        )
    creator = user_info["username"]
    list_of_users.append(user_id)
    for uid in users:
        user_id = users[uid]["user_id"]
        if user_id in list_of_users:
            member_list[user_id] = users[uid]["username"]
    print(member_list)
    chat_data = {
        chat_id: {
            security_level: {
                "chat_history": {},
                "members": member_list,
                "member_count": len(list_of_users),
                "message_count": 0,
            },
            "chat_name": chat_name,
            "creation_date": timestamp,
            "chat_description": chat_description,
            "creator": creator,
        }
    }
    db.child("chats").update(chat_data, token=user["idToken"])
    auth.create_user_with_email_and_password(
        chat_id.lower() + "@thawne.com",
        generate_key(chat_id.lower(), password.lower())[:20],
    )

    for uid in users:
        user_id = users[uid]["user_id"]
        if user_id in list_of_users:
            item = {
                "chat_name": chat_name,
                "security_level": security_level,
                "access": {"read": general_read, "write": general_write},
            }
            db.child("users").child(uid).child("chats").child(chat_id).update(
                item, token=user["idToken"]
            )
    if security_level == "Open":
        return (
            True,
            f"{chat_id} has been created by {creator}. The security level is {security_level}.",
        )
    else:
        return (
            True,
            f"{chat_id} has been created by {creator}. The security level is {security_level}. The following is the password: {password}",
        )


def delete_chat(user_id, password, chat_id):
    try:
        user = auth.sign_in_with_email_and_password(
            user_id.lower() + "@thawne.com",
            generate_key(user_id.lower(), password.lower())[:20],
        )
        if (
            db.child("users")
            .child(user["localId"])
            .child("level")
            .get(user["idToken"])
            .val()
            == "Master"
        ):
            user_list = db.child("users").get(user["idToken"]).val()
            for uid in user_list:
                if chat_id in user_list[uid]["chats"]:
                    db.child("users").child(uid).child("chats").child(chat_id).remove(
                        user["idToken"]
                    )
            db.child("chats").child(chat_id).remove(user["idToken"])
            return True, "Chat has been removed"
        else:
            return False, "Invalid User Level."
    except:
        return False, "Error in removing chat"


def queue_chat_request(
    user_id,
    password,
    action,
    chat_name,
    chat_description,
    security_level,
    list_of_users,
    general_read=True,
    general_write=True,
):
    try:
        user = auth.sign_in_with_email_and_password(
            user_id.lower() + "@thawne.com",
            generate_key(user_id.lower(), password.lower())[:20],
        )
        level = (
            db.child("users")
            .child(user["localId"])
            .child("level")
            .get(token=user["idToken"])
            .val()
        )
        if level != "user":
            try:
                request_count = (
                    db.child("chat queue")
                    .child("queue_count")
                    .get(token=user["idToken"])
                    .val()
                    + 1
                )
                queue_count = (
                    db.child("chat queue")
                    .child("request_count")
                    .get(token=user["idToken"])
                    .val()
                    + 1
                )
                username = db.child("users").child(user["localId"]).child("username").get(token=user["idToken"]).val()
            except:
                request_count = 1
                queue_count = 1
            request = {
                (request_count): {
                    "action": action,
                    "chat_name": chat_name,
                }
            }
            if action == "Create":
                request[request_count]["chat_description"] = chat_description
                request[request_count]["security_level"] = security_level
                request[request_count]["list_of_users"] = list_of_users
                request[request_count]["general_read"] = general_read
                request[request_count]["general_write"] = general_write
                request[request_count]["request_id"] = request_count
                request[request_count]["request_user"] = username
                request[request_count]["request_user_id"] = user_id
            elif action == "Delete":
                pass
            db.child("chat queue").child("queue").update(request, token=user["idToken"])
            db.child("chat queue").child("queue_count").set(
                queue_count, token=user["idToken"]
            )
            db.child("chat queue").child("request_count").set(
                request_count, token=user["idToken"]
            )
            return True, "Queue Successfully Added."
        else:
            return False, "User not authorized to create chats."
    except Exception as e:
        return False, e


def resolve_chat_queue(user_id, password, request_id):
    try:
        user = auth.sign_in_with_email_and_password(
            user_id.lower() + "@thawne.com",
            generate_key(user_id.lower(), password.lower())[:20],
        )
        request = (
            db.child("chat queue")
            .child("queue")
            .child(request_id)
            .get(token=user["idToken"])
            .val()
        )
        if request["action"] == "Create":
            state, message = create_chat(
                user_id,
                password,
                chat_name=request["chat_name"],
                chat_description=request["chat_description"],
                security_level=request["security_level"],
                list_of_users=request["list_of_users"],
                general_read=request["general_read"],
                general_write=request["general_write"],
            )
            request["Approved by"] = user_id
            db.child("chat queue").child("history").child(request_id).update(
                request, token=user["idToken"]
            )
        elif request["action"] == "Delete":
            state, message = delete_chat(user_id, password, request["chat_name"])
            db.child("chat queue").child("history").child(request_id).update(
                request, token=user["idToken"]
            )
        if state:
            db.child("chat queue").child("queue").child(request_id).remove(token=user["idToken"])
            return True, message
        return False, message
    except Exception as e:
        return False, e


def augment_user(user_id, password, subject_user_id, keyword):
    try:
        user = auth.sign_in_with_email_and_password(
            user_id.lower() + "@thawne.com",
            generate_key(user_id.lower(), password.lower())[:20],
        )
        user_level = (
            db.child("users")
            .child(user["localId"])
            .child("level")
            .get(token=user["idToken"])
            .val()
        )
        if user_level == "Master":
            user_list = db.child("users").get(token=user["idToken"]).val()
            for users in user_list:
                if user_list[users]["user_id"] == subject_user_id:
                    db.child("users").child(users).child("status").update(
                        keyword, token=user["idToken"]
                    )
                    return True, f"User has been {keyword}"
            return False, "Target user not found."
        return False, "Current user not authorized to augment users."
    except Exception as e:
        return False, e


def queue_augment_user(user_id, password, subject_user_id, keyword):
    try:
        user = auth.sign_in_with_email_and_password(
            user_id.lower() + "@thawne.com",
            generate_key(user_id.lower(), password.lower())[:20],
        )
        try:
            request_count = (
                db.child("user augment queue")
                .child("queue_count")
                .get(token=user["idToken"])
                .val()
                + 1
            )
            queue_count = (
                db.child("user augment queue")
                .child("request_count")
                .get(token=user["idToken"])
                .val()
                + 1
            )
        except:
            request_count = 1
            queue_count = 1
        request = {
            request_count: {"subject_user_id": subject_user_id, "keyword": keyword}
        }
        db.child("user augment queue").child("queue").update(
            request, token=user["idToken"]
        )
        db.child("user augment queue").child("queue_count").set(
            queue_count, token=user["idToken"]
        )
        db.child("user augment queue").child("request_count").set(
            request_count, token=user["idToken"]
        )
    except Exception as e:
        return False, e


def resolve_augment_user(user_id, password, request_id):
    try:
        user = auth.sign_in_with_email_and_password(
            user_id.lower() + "@thawne.com",
            generate_key(user_id.lower(), password.lower())[:20],
        )
        request = (
            db.child("user augment queue")
            .child("queue")
            .child(request_id)
            .get(token=user["idToken"])
            .val()
        )
        state, message = augment_user(
            user_id, password, request["subject_user_id"], request["keyword"]
        )
        if state:
            return True, message
        return False, message
    except Exception as e:
        return False, e


def retrieve_chat_queue(user_id, password):
    try:
        user = auth.sign_in_with_email_and_password(
            user_id.lower() + "@thawne.com",
            generate_key(user_id.lower(), password.lower())[:20],
        )
        history = db.child("chat queue").child("queue").get(token=user["idToken"]).val()
        return True, history
    except Exception as e:
        return False, e

def retrieve_user_augment_queue(user_id, password):
    try:
        user = auth.sign_in_with_email_and_password(
            user_id.lower() + "@thawne.com",
            generate_key(user_id.lower(), password.lower())[:20],
        )
        history = db.child("user augment queue").child("queue").get(token=user["idToken"]).val()
        return True, history
    except Exception as e:
        return False, e