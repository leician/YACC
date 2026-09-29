import logging

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSplitter,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ui.console import ConsoleWidget
from ui.settings import SettingsMenu
from util.logger import QtLogHandler


class CrosshairPreview(QLabel):
    def __init__(self, image_path):
        super().__init__()
        self.image = QPixmap(image_path)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.image.isNull():
            self.setText("crosshair preview")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.image.isNull():
            self.setPixmap(
                self.image.scaled(
                    self.contentsRect().size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.setWindowTitle("Yet Another Crosshair Changer")
        self.resize(960, 540)
        self.setMinimumSize(QSize(960, 540))
        self.setWindowIcon(QIcon('assets/app.ico'))

        options_button = QToolButton()
        options_button.setText("Options")
        options_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        options_button.setAutoRaise(True)
        options_button.setFixedSize(QSize(50, 30))
        options_button.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )
        options_menu = QMenu(options_button)
        options_menu.addAction("Settings...", self.open_settings)
        options_button.setMenu(options_menu)

        about_button = QToolButton()
        about_button.setText("About")
        about_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        about_button.setAutoRaise(True)
        about_button.setFixedSize(QSize(50, 30))
        about_button.clicked.connect(self.open_about)

        header = QHBoxLayout()
        header.setContentsMargins(8, 0, 8, 0)
        header.setSpacing(4)
        header.addWidget(options_button)
        header.addWidget(about_button)
        header.addStretch()

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addLayout(header)
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setContentsMargins(0, 4, 4, 0)
        layout.addWidget(separator)
        layout.addWidget(self.create_crosshair_page())

        self.setCentralWidget(central)

    def open_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.resize(720, 480)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(SettingsMenu(dialog))
        dialog.exec()

    def open_about(self):
        QMessageBox.about(
            self,
            "About Yet Another Crosshair Changer",
            "Yet Another Crosshair Changer",
        )

    def section(self, title, widget=None, button=None):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 8, 8, 8)

        header = QHBoxLayout()
        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header.addWidget(label)
        header.addStretch()

        if button is not None:
            header.addWidget(button)

        layout.addLayout(header)

        if widget is not None:
            layout.addWidget(widget)

        return panel

    def create_crosshair_page(self):
        self.log_handler = QtLogHandler()
        self.log_handler.setFormatter(
            logging.Formatter(
                "%(message)s"
            )
        )
        logging.getLogger().addHandler(self.log_handler)
        logging.getLogger().setLevel(logging.INFO)

        logs = ConsoleWidget()
        self.log_handler.emitter.message.connect(
            logs.append_log
        )
        left_column = self.section("logs", logs)

        preview = QWidget()
        preview_layout = QVBoxLayout(preview)
        preview_label = CrosshairPreview("assets/placeholder.png")
        preview_layout.addWidget(preview_label)

        weapon_selector = QComboBox()
        weapon_selector.addItem("select weapon")
        weapon_selector.addItems(["Scattergun", "Rocket Launcher", "Pistol"])

        crosshair_selector = QComboBox()
        crosshair_selector.addItem("pick crosshair")
        crosshair_selector.addItems(["Wings", "X", "Cross"])

        add_crosshairs = QPushButton("add")
        loaded_crosshairs = QListWidget()
        loaded_crosshairs.addItems(["Wings", "X", "Cross"])

        controls = QHBoxLayout()
        controls.addWidget(weapon_selector, 4)
        controls.addWidget(crosshair_selector, 3)
        controls.addWidget(add_crosshairs, 1)

        lower_area = QWidget()
        lower_layout = QVBoxLayout(lower_area)
        lower_layout.setContentsMargins(8, 8, 8, 8)

        controls_row = QWidget()
        controls_row.setLayout(controls)
        controls_layout = QHBoxLayout()
        lower_layout.addLayout(controls_layout)
        controls_layout.addWidget(controls_row, 2)
        controls_layout.addStretch(1)
        lower_layout.addWidget(loaded_crosshairs)

        right_splitter = QSplitter(Qt.Orientation.Vertical)
        right_splitter.addWidget(preview)
        right_splitter.addWidget(lower_area)
        right_splitter.setSizes([250, 830])

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.addWidget(left_column)
        main_splitter.addWidget(right_splitter)
        main_splitter.setSizes([590, 1330])

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(main_splitter)

        return page