import os
import sys
from PyQt5 import QtWebEngineWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QToolBar, QDialog, QLabel, \
    QLineEdit, QSizePolicy, QLayout, QGridLayout, QColorDialog

from Game import logic


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.field = GameField()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        self.settings_window = SettingsWindow()
        self.settings_window.color_changed.connect(self.change_background_color)
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings_window)

        self.instruction_window = InstructionsWindow()
        self.instruction_button = QPushButton("Instruction")
        self.instruction_button.clicked.connect(self.open_instruction_window)

        toolbar = QToolBar()
        toolbar.addWidget(self.settings_button)
        toolbar.addWidget(self.instruction_button)
        self.addToolBar(toolbar)
        self.layout.addWidget(self.field)

    def open_settings_window(self):
        self.settings_window.exec_()

    def open_instruction_window(self):
        self.instruction_window.exec_()

    def change_background_color(self, color):
        self.setStyleSheet(f"QMainWindow {{background-color: {color.name()};}}")


class SettingsWindow(QDialog):
    color_changed = QtCore.pyqtSignal(QtGui.QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
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

        self.color_button = QPushButton("Choose color")
        self.color_button.clicked.connect(self.choose_color)
        self.color_label = QLabel("Background Color")
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(32, 32)

        self.layout.addWidget(self.color_label)
        self.layout.addWidget(self.color_button)
        self.layout.addWidget(self.color_preview)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_preview.setPalette(QtGui.QPalette(color))
            self.color_changed.emit(color)

    def apply_grid_size(self):
        grid_size = int(self.grid_size_edit.text())


class GameField(QWidget):

    def __init__(self):
        super().__init__()
        self.settings_window = None
        self.game = logic.Game()
        self.grid = QGridLayout()
        self.grid.setSizeConstraint(QLayout.SetMinimumSize)
        self.init_ui()
        self.current_button = None

    def init_ui(self):
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for row in range(len(self.game.arr)):
            for col in range(len(self.game.arr[0])):
                index_of_image = str(self.game.arr[row][col])
                button = SquareButton(index_of_image)
                button.setMinimumSize(QtCore.QSize(50, 50))
                button.clicked.connect(lambda checked, row=row, col=col: self.on_button_clicked(row, col))
                button.setSizePolicy(size_policy)
                self.grid.addWidget(button, row, col)

        self.setLayout(self.grid)
        self.setGeometry(100, 100, 300, 300)
        self.show()

    def on_button_clicked(self, row, col):
        if self.current_button:
            if self.current_button[2].index_of_image != self.sender().index_of_image:
                self.grid = self.layout()
                pos1 = self.grid.indexOf(self.current_button[2])
                pos2 = self.grid.indexOf(self.sender())
                row1, col1, _, _ = self.grid.getItemPosition(pos1)
                row2, col2, _, _ = self.grid.getItemPosition(pos2)
                if self.game.swap_heart(row1, col1, row2, col2):
                    self.update_grid()
                    self.grid.update()
        self.current_button = (row, col, self.sender())

    def update_grid(self):
        for i in range(self.grid.count()):
            item = self.grid.itemAt(i).widget()
            item.update_image(self.game.arr[i // 8][i % 8])


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


class SquareButton(QPushButton):
    def __init__(self, index_of_image):
        super().__init__()
        self._index_of_image = None
        self.image = None
        self.update_image(index_of_image)

    def sizeHint(self):
        size = super().sizeHint()
        max_dimension = max(size.width(), size.height())
        return QtCore.QSize(max_dimension, max_dimension)

    def update_image(self, index_of_image):
        self.index_of_image = index_of_image
        self.image = QtGui.QPixmap(os.path.abspath(f"images/image{self.index_of_image}"))
        size = self.size()
        self.image = self.image.scaled(size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        icon = QtGui.QIcon(self.image)
        self.setIcon(icon)

        policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(policy)

    @property
    def index_of_image(self):
        return self._index_of_image

    @index_of_image.setter
    def index_of_image(self, value):
        self._index_of_image = value


app = QApplication(['', "--no-sandbox"])
window = MainFrame()
window.show()
sys.exit(app.exec_())
