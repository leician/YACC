import sys

from ui.style import stylesheet
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    app.setStyleSheet(stylesheet)
    
    window.show()
    app.exec()