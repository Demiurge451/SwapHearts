import os

from PyQt5 import QtWebEngineWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QVBoxLayout


class InstructionsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instructions")

        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.load(QtCore.QUrl().fromLocalFile(
            os.path.split(os.path.abspath(__file__))[0] + r'\html\instruction.html'
        ))
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
