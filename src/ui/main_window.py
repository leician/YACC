from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QLabel,
    QMainWindow,
    QTextEdit,
    QListWidget,
    QPushButton
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Yet Another Crosshair Changer")
        self.resize(960,540)
        self.setMinimumSize(QSize(960,540))
        self.setWindowIcon(QIcon('assets/app.ico'))

        tabs = QTabWidget()
        tabs.addTab(self.create_crosshair_tab(), "Crosshairs")
        tabs.addTab(QWidget(), "Settings")
        tabs.addTab(QWidget(), "About")
        
        self.setCentralWidget(tabs)
        self.create_crosshair_tab()

    def section(self, title, widget = None):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8,8,8,8)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(label)

        if widget is not None:
            layout.addWidget(widget)

        return panel

    def create_crosshair_tab(self):
        logs = QTextEdit()
        logs.setReadOnly(True)
        left_column = self.section("> Logs", logs)

        applied_crosshair = self.section("applied crosshair")
        weapons = QListWidget()
        weapons.addItems(
            ["1", "2", "3"]
        )
        weapon_list = self.section("> Weapons", weapons)

        center_splitter = QSplitter(Qt.Orientation.Vertical)
        center_splitter.addWidget(applied_crosshair)
        center_splitter.addWidget(weapon_list)
        center_splitter.setSizes([200,400])

        preview = self.section("crosshair preview")
        loaded_crosshairs = QListWidget()
        loaded_crosshairs.addItems(
            ["1", "2", "3"]
        )
        crosshair_list = self.section("> Available crosshairs", loaded_crosshairs)

        right_splitter = QSplitter(Qt.Orientation.Vertical)
        right_splitter.addWidget(preview)
        right_splitter.addWidget(crosshair_list)
        right_splitter.setSizes([200,400])

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.addWidget(left_column)
        main_splitter.addWidget(center_splitter)
        main_splitter.addWidget(right_splitter)
        main_splitter.setSizes([220,390,390])

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(main_splitter)

        return page