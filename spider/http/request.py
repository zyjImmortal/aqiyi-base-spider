

class Request:

    def __init__(self, url, method, params=None, data=None, headers=None):
        self.url = url
        self.method = method
        self.params = params or {}
        self.data = data or {}
        self.headers = headers or {}