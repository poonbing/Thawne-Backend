from flask_socketio import Namespace, emit
from .filequeue import FileQueue
from .utils import file_scan
import threading


class FileScanNamespace(Namespace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filequeue = FileQueue()

    def on_queue_file(self, data):
        self.filequeue.enqueue(data)
        threading.Thread(target=self.process_queue).start()

    def process_queue(self):
        while not self.filequeue.is_empty():
            file_data = self.filequeue.dequeue()
            state, log, counter = self.run_file_scan(file_data)
            if state:
                emit("return_all_chats", counter)
                return
            else:
                emit("error_all_chats", counter)
                return

    def run_file_scan(self, file_data):
        return file_scan(
            file_data["user_id"],
            file_data["password"],
            file_data["filename"],
            file_data["file_security"],
        )
