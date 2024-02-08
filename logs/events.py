from flask_socketio import Namespace, emit
from .utils import log_event, retrieve_log_queue
import json
from utils.cryptography import encrypt_data


class LogsNamespace(Namespace):
    def on_log_event(self, data):
        status, message = log_event(data.get('userId'), data.get('password'), data.get('type'), data.get('location'), data.get('context'))
        # message = encrypt_data(json.dumps(message))
        if status:
            emit('return_log_event', message)
        else:
            emit('error_log_event', message)
    
    def on_retrieve_new_logs(self, data):
        status, message = retrieve_log_queue(data.get('userId'), data.get('password'))