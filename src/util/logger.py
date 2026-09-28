import logging
from typing import TextIO

from PySide6.QtCore import QObject, Signal


class LogEmitter(QObject):
    message = Signal(str)

class QtLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.emitter = LogEmitter()

    def emit(self, record):
        try:
            message = self.format(record)
            self.emitter.message.emit(message)
        except Exception:
            self.handleError(record)