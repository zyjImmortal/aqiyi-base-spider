class Request:

    def __init__(self, url, method='GET', params=None, data=None, headers=None, callback=None):
        self.url = url
        self.method = method
        self.params = params or {}
        self.data = data or {}
        self.headers = headers or {}
        self.callback = callback
