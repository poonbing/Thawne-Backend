from flask_socketio import Namespace, emit
from .utils import log_event


class LogsNamespace(Namespace):
    def on_log_event(data):
        status, message = log_event(data.get('userId'), data.get('password'), data.get('type'), data.get('location'), data.get('context'))
        if status:
            emit('return_log_event', message)
            return
        emit('error_log_event', message)
        return