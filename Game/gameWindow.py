import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
import logic
import settings


# TODO add diapason
class GameField(QWidget):
    def __init__(self):
        super().__init__()
        self.settings_window = None
        self.game = logic.Game()
        self.grid = QGridLayout()
        self.init_ui()
        self.current_button = None

    def init_ui(self):
        for row in range(len(self.game.arr)):
            for col in range(len(self.game.arr[0])):
                button = QPushButton(str(self.game.arr[row][col]))
                button.setFixedSize(50, 50)
                button.clicked.connect(lambda checked, row=row, col=col: self.on_button_clicked(row, col))
                self.grid.addWidget(button, row, col)

        self.setLayout(self.grid)
        self.setGeometry(100, 100, 300, 300)
        self.show()

    def on_button_clicked(self, row, col):
        if self.current_button is None:
            # First button clicked
            self.current_button = (row, col, self.sender())
        else:
            # Second button clicked - swap buttons if labels match
            if self.current_button[2].text() != self.sender().text():
                self.grid = self.layout()
                pos1 = self.grid.indexOf(self.current_button[2])
                pos2 = self.grid.indexOf(self.sender())
                row1, col1, _, _ = self.grid.getItemPosition(pos1)
                row2, col2, _, _ = self.grid.getItemPosition(pos2)
                if self.game.swap_heart(row1, col1, row2, col2):
                    self.update_grid()
                    self.grid.update()

            self.current_button = None

    def update_grid(self):
        for i in range(self.grid.count()):
            item = self.grid.itemAt(i).widget()
            item.setText(str(self.game.arr[i // 8][i % 8]))


