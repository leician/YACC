import logging

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


class BufferedLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []
        self.target = None

    def emit(self, record):
        if self.target is None:
            self.records.append(record)
        else:
            self.target.handle(record)

    def set_target(self, target):
        self.acquire()
        try:
            for record in self.records:
                target.handle(record)
            self.records.clear()
            self.target = target
        finally:
            self.release()