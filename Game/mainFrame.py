import os
import sys
from PyQt5 import QtWebEngineWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QToolBar, QDialog, QLabel, \
    QLineEdit, QSizePolicy, QLayout, QGridLayout, QColorDialog, QHBoxLayout

from Game import logic
from Game.settings import SettingsWindow


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.score_label = ScoreLabel(0)
        self.score_label.setStyleSheet("""
            QLabel {
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: qradialgradient(
                    cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 #fff, stop: 1 #bbb
                );
                font-size: 20px;
                font-weight: bold;
            }
            QLabel:hover {
                background-color: qradialgradient(
                    cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 #fff, stop: 1 #ddd
                );
            }
        """)
        self.layout = QVBoxLayout()
        self.field = GameField()
        self.field.score_changed.connect(self.score_label.update_score)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        self.settings_window = SettingsWindow(self)
        self.settings_window.color_changed.connect(self.change_background_color)
        self.settings_button = MyButton("Settings")
        self.settings_button.clicked.connect(self.open_settings_window)

        self.instruction_window = InstructionsWindow()
        self.instruction_button = MyButton("Instruction")
        self.instruction_button.clicked.connect(self.open_instruction_window)

        toolbar = QToolBar()
        toolbar.addWidget(self.settings_button)
        toolbar.addWidget(self.instruction_button)
        self.addToolBar(toolbar)

        header = QHBoxLayout()
        self.new_game_button = MyButton("New Game")
        self.new_game_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.new_game_button.setMaximumSize(200, 50)

        self.new_game_button.clicked.connect(self.start_new_game)

        header.addWidget(self.new_game_button)
        header.addStretch()
        header.addWidget(self.score_label)
        self.layout.addLayout(header)
        self.layout.addWidget(self.field)

    def start_new_game(self):
        self.field.new_game()

    def open_settings_window(self):
        self.settings_window.exec_()

    def open_instruction_window(self):
        self.instruction_window.exec_()

    def change_background_color(self, color):
        self.setStyleSheet(f"QMainWindow {{background-color: {color.name()};}}")


class MyButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        size = int(min(self.width(), self.height()) * 2)
        self.setIconSize(QtCore.QSize(size, size))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = int(min(self.width(), self.height()) * 2)
        self.setIconSize(QtCore.QSize(size, size))


class GameField(QWidget):
    score_changed = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.score = 0
        self.settings_window = None
        self.game = logic.Game()
        self.grid = QGridLayout()
        self.grid.setSizeConstraint(QLayout.SetMinimumSize)
        self.current_button = None
        self.init_ui()

    def init_ui(self):
        for row in range(len(self.game.arr)):
            for col in range(len(self.game.arr[0])):
                index_of_image = str(self.game.arr[row][col])
                button = GridButton(index_of_image)
                button.setBaseSize(QtCore.QSize(50, 50))
                button.clicked.connect(lambda checked, row=row, col=col: self.on_button_clicked(row, col))
                self.grid.addWidget(button, row, col)

        self.setLayout(self.grid)
        self.setGeometry(100, 100, 300, 300)

    def on_button_clicked(self, row, col):
        if self.current_button is None:
            self.current_button = (row, col, self.sender())
        else:
            if self.current_button[2].index_of_image != self.sender().index_of_image:
                self.grid = self.layout()
                pos1 = self.grid.indexOf(self.current_button[2])
                pos2 = self.grid.indexOf(self.sender())
                row1, col1, _, _ = self.grid.getItemPosition(pos1)
                row2, col2, _, _ = self.grid.getItemPosition(pos2)
                cur_score = self.game.swap_heart(row1, col1, row2, col2)
                if cur_score != 0:
                    self.update_grid()
                    self.score += cur_score

            self.current_button = None

    def update_grid(self):
        for i in range(self.grid.count()):
            item = self.grid.itemAt(i).widget()
            item.update_image(self.game.arr[i // 8][i % 8])
        self.grid.update()

    def new_game(self):
        self.game = logic.Game()
        self.score = 0
        self.update_grid()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self.score_changed.emit(self._score)


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


class GridButton(QPushButton):
    def __init__(self, index_of_image):
        super().__init__()
        self._index_of_image = None
        self.image_label = QLabel()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.image_label)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.update_image(index_of_image)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def update_image(self, index_of_image):
        self.index_of_image = index_of_image
        image = QtGui.QPixmap(os.path.abspath(f"images/image{self.index_of_image}"))
        size = self.size()
        image = image.scaled(size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.image_label.setPixmap(image)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resizeEvent(self, event):
        self.update_image(self.index_of_image)
        super().resizeEvent(event)

    @property
    def index_of_image(self):
        return self._index_of_image

    @index_of_image.setter
    def index_of_image(self, value):
        self._index_of_image = value


class ScoreLabel(QLabel):
    def __init__(self, score):
        super().__init__()
        self.score = score
        self.setText(f"Score: {score}")

    @QtCore.pyqtSlot(int)
    def update_score(self, score):
        self.score = score
        self.setText(f"Score: {score}")


app = QApplication(['', "--no-sandbox"])
window = MainFrame()
window.show()
sys.exit(app.exec_())
