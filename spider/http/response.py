class Response:

    def __init__(self, url, body, status=200, headers=None, request=None):
        self.headers = headers or {}
        self.status = int(status)
        self._set_body(body)
        self._set_url(url)
        self.request = request

    def _set_body(self, body):
        if body is None:
            self._body = ''
        elif not isinstance(body, str):
            raise TypeError("Response body must be str")
        else:
            self._body = body

    def _set_url(self, url):
        if isinstance(url, str):
            self._url = url
        else:
            raise TypeError("%s url must be str, got %s:".format(
                type(self).__name__, type(url).__name__))

    @property
    def url(self):
        return self._url

    @property
    def body(self):
        return self._body

    def json(self):
        pass

    def xpath(self):
        pass
