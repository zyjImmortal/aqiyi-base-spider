from spider.http.request import Request


class Spider:
    start_urls = []

    def start_request(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        raise NotImplementedError()
