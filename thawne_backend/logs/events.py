from flask_socketio import Namespace, emit
from .utils import log_event, retrieve_log_queue


class LogsNamespace(Namespace):
    def on_log_event(self, data):
        status, message = log_event(data.get('userId'), data.get('password'), data.get('type'), data.get('location'), data.get('context'))
        if status:
            emit('return_log_event', message)
            return
        emit('error_log_event', message)
        return
    
    def on_retrieve_new_logs(self, data):
        status, message = retrieve_log_queue(data.get('userId'), data.get('password'))