import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.style import stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    app.setStyleSheet(stylesheet)
    
    window.show()
    app.exec()