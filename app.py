from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from authenticate.events import AuthenticateNamespace
from authenticate.utils import login_check
from chat.events import ChatNamespace
from operation.events import OperationNamespace
from logs.events import LogsNamespace, DataLayer
from file_scan.events import FileScanNamespace
from logs.report import ReportGeneration


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")


socketio.on_namespace(AuthenticateNamespace("/auth"))
socketio.on_namespace(ChatNamespace("/chat"))
socketio.on_namespace(OperationNamespace("/operation"))
socketio.on_namespace(LogsNamespace("/log"))
socketio.on_namespace(FileScanNamespace("/filescan"))
report = ReportGeneration(app, DataLayer("thawne.owner", "UM77682@root"))


@app.route("/")
def default():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app=app)
