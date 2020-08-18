import sys
from logging import StreamHandler, Formatter

from deviceservice.producer import produce_log


class LoggingHandler(StreamHandler):
    """ Extends the default handler so that we can produce a kafka log message as
        well as a regular log. """

    def __init__(self):
        super().__init__(sys.stderr)
        self.formatter = Formatter('[%(asctime)s] %(levelname)s: %(message)s')

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg + self.terminator)
            self.flush()
            produce_log(msg)
        except Exception:
            self.handleError(record)
