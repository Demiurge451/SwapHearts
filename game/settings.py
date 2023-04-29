from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QColorDialog, QSpinBox, QHBoxLayout, QApplication


class SettingsWindow(QDialog):
    color_changed = QtCore.pyqtSignal(QtGui.QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(250, 100)
        self.setWindowTitle("Settings")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.width_label = QLabel("Width:")
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(parent.width(), QApplication.desktop().width())
        self.width_spinbox.setSingleStep(10)
        self.height_label = QLabel("Height:")
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(parent.height(), QApplication.desktop().height())
        self.height_spinbox.setSingleStep(10)

        width_layout = QHBoxLayout()
        width_layout.addWidget(self.width_label)
        width_layout.addWidget(self.width_spinbox)
        height_layout = QHBoxLayout()
        height_layout.addWidget(self.height_label)
        height_layout.addWidget(self.height_spinbox)
        button_layout = QHBoxLayout()
        main_layout = QVBoxLayout()
        main_layout.addLayout(width_layout)
        main_layout.addLayout(height_layout)
        main_layout.addLayout(button_layout)

        # Set the dialog layout
        self.layout.addLayout(main_layout)

        self.color_button = QPushButton("Choose color")
        self.color_button.clicked.connect(self.choose_color)
        self.color_label = QLabel("Background Color")

        self.layout.addWidget(self.color_label)
        self.layout.addWidget(self.color_button)

        self.width_spinbox.valueChanged.connect(self.set_size_x)
        self.height_spinbox.valueChanged.connect(self.set_size_y)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_changed.emit(color)

    def set_size_x(self, value):
        self.parent().resize(value, self.parent().height())

    def set_size_y(self, value):
        self.parent().resize(self.parent().width(), value)
