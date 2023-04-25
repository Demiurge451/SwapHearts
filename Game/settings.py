from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.grid_size_label = QLabel("Grid Size:")
        self.grid_size_edit = QLineEdit()
        self.grid_size_edit.setText("10")
        self.grid_size_button = QPushButton("Apply")
        self.grid_size_button.clicked.connect(self.apply_grid_size)
        self.layout.addWidget(self.grid_size_label)
        self.layout.addWidget(self.grid_size_edit)
        self.layout.addWidget(self.grid_size_button)

    def apply_grid_size(self):
        grid_size = int(self.grid_size_edit.text())

