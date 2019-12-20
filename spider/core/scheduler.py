
from queue import Queue


class Scheduler:


    def __init__(self):
        self._queue = Queue()

    def add_request(self, request):
        self._queue.put(request)

    def get_request(self):
        return self._queue.get_nowait()

    def _filter_request(self):
        pass