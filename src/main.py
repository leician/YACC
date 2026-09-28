from ui import MainWindow
from PySide6.QtWidgets import QApplication
import qt_themes
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    qt_themes.set_theme("nord")

    app.setStyleSheet("""
        QSplitter::handle {
            background: #555;
        }

        QSplitter::handle:hover {
            background: #888;
        }
    """)
    
    window.show()
    app.exec()