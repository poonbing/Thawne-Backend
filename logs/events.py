from flask_socketio import Namespace, emit
from .utils import log_event, retrieve_log_queue
import json
from utils.cryptography import encrypt_data


class LogsNamespace(Namespace):
    def on_log_event(self, data):
        print(data)
        userId = data.get('userId')
        password = data.get('password')
        type = data.get('type')
        location = data.get('location')
        context = data.get('context')
        if password == False:
            password = 'false'
        status, message = log_event(userId, password, type, location, context)
        # message = encrypt_data(json.dumps(message))
        if status:
            emit('return_log_event', message)
        else:
            emit('error_log_event', message)
    
    def on_retrieve_new_logs(self, data):
        status, message = retrieve_log_queue(data.get('userId'), data.get('password'))