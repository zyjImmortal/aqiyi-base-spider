import requests
import json


class Downloader:

    def request(self, url, method, params=None, data=None, headers=None):
        response = None
        if method == 'GET':
            response = requests.get(url, params, headers=headers).content
        elif method == 'POST':
            response = requests.post(url, json=json.dumps(data), headers=headers)
        return response
