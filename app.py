from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from authenticate.events import AuthenticateNamespace
from chat.events import ChatNamespace
from operation.events import OperationNamespace
from logs.events import LogsNamespace
from file_scan.events import FileScanNamespace


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")



socketio.on_namespace(AuthenticateNamespace("/auth"))
socketio.on_namespace(ChatNamespace("/chat"))
socketio.on_namespace(OperationNamespace("/operation"))
socketio.on_namespace(LogsNamespace("/log"))
socketio.on_namespace(FileScanNamespace("/filescan"))


@app.route("/")
def default():
    return render_template("index.html")


@app.route("/ping")
def hello_world():
    return "pong"



if __name__ == "__main__":
    socketio.run(app=app, port=5000, debug=True)
