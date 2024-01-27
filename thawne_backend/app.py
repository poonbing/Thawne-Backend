from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from authenticate.events import AuthenticateNamespace
from chat.events import ChatNamespace
from operation.events import OperationNamespace
from logs.events import LogsNamespace


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")


socketio.on_namespace(AuthenticateNamespace('/auth'))
socketio.on_namespace(ChatNamespace('/chat'))
socketio.on_namespace(OperationNamespace('/operation'))
socketio.on_namespace(LogsNamespace('/log'))


if __name__ == "__main__":
    socketio.run(app, debug=True)
