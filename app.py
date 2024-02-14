from flask import Flask, render_template, request, url_for, redirect, flash
from flask_cors import CORS
from flask_socketio import SocketIO
from authenticate.events import AuthenticateNamespace
from authenticate.utils import login_check
from chat.events import ChatNamespace
from operation.events import OperationNamespace
from operation.utils import retrieve_chat_queue, resolve_chat_queue, retrieve_user_augment_queue, resolve_augment_user
from logs.events import LogsNamespace
from logs.utils import retrieve_log_queue
from file_scan.events import FileScanNamespace


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


socketio.on_namespace(AuthenticateNamespace("/auth"))
socketio.on_namespace(ChatNamespace("/chat"))
socketio.on_namespace(OperationNamespace("/operation"))
socketio.on_namespace(LogsNamespace("/log"))
socketio.on_namespace(FileScanNamespace("/filescan"))


@app.route("/", methods=["POST"])
def default():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def initiate_login():
    user_id = request.get('userId')
    password = request.get('pass')
    status, message = login_check(user_id, password)
    if status:
        return redirect(url_for("load_log_queue", request={'userId':user_id, 'pass':password}))

@app.route("/viewlogs", methods=["POST"])
def load_log_queue():
    user_id = request.get('userId')
    password = request.get('pass')
    status, message = retrieve_log_queue(user_id, password)
    if status:
        return render_template("logs.html", logs=message)
    
@app.route("/chats", methods=["POST"])
def load_chat_requests():
    # user_id = request.get('userId')
    # password = request.get('pass')
    status, message = retrieve_chat_queue("UM77682", "poonbing@root")
    print(message)

    chat_attributes = message
    
    return render_template("chat_log.html", chat_attributes=chat_attributes)
    

@app.route("/chat/resolve/<string:id>", methods=["GET", "POST"])
def resolve_chat_requests(id): 
    # user_id = request.get('userId')
    # password = request.get('pass')
    # request_id = request.get('reqId')
    status, _ = resolve_chat_queue("UM77682", "poonbing@root", id)
    if status:
        flash(f'Chat with id {id} has been created')
        return redirect(url_for('load_chat_requests'))
    else:
        flash(f'Something went wrong.')
        return redirect(url_for('load_chat_requests'))
    
@app.route("/users", methods=["POST"])
def load_user_augment_requests():
    user_id = request.get('userId')
    password = request.get('pass')
    status, message = retrieve_user_augment_queue(user_id, password)
    if status:
        return render_template("user_log.html", requests=message)

@app.route("/chat/resolve", methods=["POST"])
def resolve_user_augment_requests():
    user_id = request.get('userId')
    password = request.get('pass')
    request_id = request.get('reqId')
    status, _ = resolve_augment_user(user_id, password, request_id)
    if status:
        return redirect(url_for('load_user_augment_requests', request={'userId':user_id, 'pass':password}))


if __name__ == "__main__":
    socketio.run(app=app)
