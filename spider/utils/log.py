import datetime
import logging
import os
from logging.handlers import BaseRotatingHandler
from spider.config.settings import LOG

class SpiderRotatingFileHandler(BaseRotatingHandler):
    """
    日志按时间切割
    """

    def __init__(self, log_dir='logs', mode='a', max_bytes=0, encoding=None, delay=False):

        if max_bytes > 0:
            mode = 'a'
        self._log_dir = log_dir
        self._suffix = ".log"
        self._year_month = datetime.datetime.now().strftime("%Y-%m")
        self.store_dir = os.path.join(self._log_dir, self._year_month)
        self._create_new_stream_if_not_exists(self.store_dir, open_stream=False)
        self.filename = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(self.store_dir, self.filename) + self._suffix
        BaseRotatingHandler.__init__(self, filename,
                                     mode, encoding, delay)
        self.max_bytes = max_bytes

    def doRollover(self):
        year_month = datetime.datetime.now().strftime("%Y-%m")
        filename = datetime.datetime.now().strftime("%Y-%m-%d")

        if self.stream:
            self.stream.close()
            self.stream = None

        if self.filename != filename or self._year_month != year_month:
            self.baseFilename = self.baseFilename.replace(
                os.path.join(self._year_month, self.filename),
                os.path.join(year_month, filename))
            self.filename = filename
            self._year_month = year_month
        else:
            dfn = self.rotation_filename(
                self.baseFilename.replace(
                    self._suffix,
                    '-' + datetime.datetime.now().strftime("%H-%M-%S") + self._suffix
                )
            )
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()

    def shouldRollover(self, record):
        year_month = datetime.datetime.now().strftime("%Y-%m")
        filename = datetime.datetime.now().strftime("%Y-%m-%d")
        self._create_new_stream_if_not_exists(os.path.join(self._log_dir, year_month))
        if self.stream is None:
            self.stream = self._open()
        if self._year_month != year_month or self.filename != filename:
            return 1
        if self.max_bytes > 0:
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.max_bytes:
                return 1
        return 0

    def _create_new_stream_if_not_exists(self, store_dir, open_stream=True):
        if not os.path.exists(store_dir):
            os.makedirs(store_dir)
            if open_stream:
                self.stream = self._open()


class Logger:

    def __init__(self, fmt=None, handler=None):
        self._fmt = fmt
        self._handler = handler
        self._logger = None
        self._log_config = LOG
        self.set_logger()
        self.init_logger()

    def init_logger(self):
        if self._log_config['FILE']:
            fmt = logging.Formatter(
                "%(asctime)s %(levelname)s %(process)d   ---  [%(threadName)s]"
                " - %(message)s" if not self._fmt else self._fmt
            )
            logging.basicConfig(level=self._log_config.get("level", "DEBUG"))
            self._handler = SpiderRotatingFileHandler(
                log_dir=self._log_config['DIR'],
                max_bytes=self._log_config['SIZE_LIMIT'],
                encoding='UTF-8'
            )
            self._handler.setFormatter(fmt)
            self._handler.setLevel(level=self._log_config.get("level", "DEBUG"))
            self._logger.addHandler(self._handler)
        else:
            return

    def set_logger(self):
        self._logger = logging.getLogger(__name__)

    def get_logger(self):
        return self._logger


logger = Logger().get_logger()



