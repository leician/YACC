import logging
import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.style import stylesheet
from util.logger import BufferedLogHandler
from util.util import create_dirs

if __name__ == "__main__":
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    log_buffer = BufferedLogHandler()
    root_logger.addHandler(log_buffer)

    path = create_dirs()
    
    app = QApplication(sys.argv)
    window = MainWindow(log_buffer)

    app.setStyleSheet(stylesheet)
    
    window.show()
    app.exec()