import os

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QSizePolicy, QGridLayout, QLayout

from game import logic


class GameField(QWidget):
    score_changed = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.score = 0
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

