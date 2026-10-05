import logging

from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from core.config import Config


class SettingsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.logger = logging.getLogger("YACC")

        self.config_manager = Config()
        self.config = self.config_manager.read_config()
        self.path = self.config["general"]["tf_path"]

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(divider)

        body = QHBoxLayout()
        body.setContentsMargins(15, 14, 15, 14)
        body.setSpacing(10)
        root.addLayout(body, stretch=1)

        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(110)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(12, 10, 12, 10)
        self.sidebar_layout.setSpacing(4)
        body.addWidget(self.sidebar)

        self.pages = QStackedWidget()
        body.addWidget(self.pages, stretch=1)

        self._nav_buttons = []

        general_page = self.create_page()
        self.path_input, self.search_button = self.add_setting(
            general_page, "Path to tf/ folder"
        )
        general_page.layout().addStretch()

        misc_page = self.create_page()
        clear_cache_button = QPushButton("Clear cache")
        misc_page.layout().addWidget(clear_cache_button)
        misc_page.layout().addStretch()

        self.pages.addWidget(general_page)
        self.pages.addWidget(misc_page)

        self.add_sidebar_option("General", 0, active=True)
        self.add_sidebar_option("Misc.", 1)
        self.sidebar_layout.addStretch()

        footer = QHBoxLayout()
        footer.setContentsMargins(15, 0, 15, 12)
        footer.addStretch()
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)
        footer.addWidget(self.apply_button)
        root.addLayout(footer)

    def create_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        return page

    def add_sidebar_option(self, text, page_index, active=False):
        button = QPushButton(text)
        button.setCheckable(True)
        button.setChecked(active)
        button.clicked.connect(
            lambda checked=False, index=page_index: self.open_page(index)
        )
        self.sidebar_layout.addWidget(button)
        self._nav_buttons.append(button)
        return button

    def open_page(self, page_index):
        self.pages.setCurrentIndex(page_index)
        for index, button in enumerate(self._nav_buttons):
            button.setChecked(index == page_index)

    def add_setting(self, page, label_text, button_text="Search"):
        setting = QWidget()
        setting_layout = QVBoxLayout(setting)
        setting_layout.setContentsMargins(0, 0, 0, 0)
        setting_layout.setSpacing(6)

        setting_layout.addWidget(QLabel(label_text))

        controls = QHBoxLayout()
        controls.setContentsMargins(0, 0, 0, 0)
        controls.setSpacing(8)

        text_input = QLineEdit()
        text_input.setText(self.path)
        text_input.setFixedSize(300, 30)

        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.select_directory(text_input))
        controls.addWidget(text_input)
        controls.addWidget(button)
        controls.addStretch()

        setting_layout.addLayout(controls)
        setting.setFixedHeight(setting_layout.sizeHint().height())
        page.layout().addWidget(setting)

        return text_input, button

    def update_path(self, obj, text):
        obj.setText(str(text))

    def apply_settings(self):
        selected_path = self.path_input.text()
        self.config_manager.write_config("general", "tf_path", selected_path)
        self.config["general"]["tf_path"] = selected_path
        self.path = selected_path
        self.logger.info(f"Set tf/ path to {selected_path}")

    def select_directory(self, line_edit: QLineEdit):
        dialog = QFileDialog(None, windowTitle="Select tf/ folder")
        dialog.accept = lambda: QDialog.accept(dialog)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)

        dialog.exec_()
        directory = dialog.selectedFiles()
        line_edit.setText(directory[0])