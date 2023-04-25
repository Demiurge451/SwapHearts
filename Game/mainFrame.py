import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication

from Game.gameWindow import GameField
from Game.settings import SettingsWindow


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.field = GameField()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.settings_button = QPushButton("Settings")
        self.layout.addWidget(self.settings_button)
        self.settings_button.clicked.connect(self.open_settings_window)
        self.layout.addWidget(self.field)

    def open_settings_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.exec_()


app = QApplication(sys.argv)
window = MainFrame()
window.show()
sys.exit(app.exec_())
