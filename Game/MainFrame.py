import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLayoutItem
import Logic
from random import randint

arr_grid = [[randint(1, 6) for j in range(8)] for i in range(8)]
grid = QGridLayout()


# TODO add diapason
class GameField(QWidget):
    def __init__(self):
        super().__init__()


        self.init_ui()

    def init_ui(self):
        Logic.update_grid(arr_grid)
        button_labels = [[str(i) for i in j] for j in arr_grid]
        for row, row_labels in enumerate(button_labels):
            for col, label in enumerate(row_labels):
                button = QPushButton(label)
                button.setFixedSize(50, 50)
                button.clicked.connect(lambda checked, row=row, col=col: self.on_button_clicked(row, col))
                grid.addWidget(button, row, col)

        self.current_button = None

        self.setLayout(grid)
        self.setGeometry(100, 100, 300, 300)
        self.show()

    def on_button_clicked(self, row, col):
        if self.current_button is None:
            # First button clicked
            self.current_button = (row, col, self.sender())
        else:
            # Second button clicked - swap buttons if labels match
            if self.current_button[2].text() != self.sender().text():
                grid = self.layout()
                pos1 = grid.indexOf(self.current_button[2])
                pos2 = grid.indexOf(self.sender())
                row1, col1, _, _ = grid.getItemPosition(pos1)
                row2, col2, _, _ = grid.getItemPosition(pos2)
                if Logic.swap_heart(row1, col1, row2, col2, arr_grid) != 0:
                    grid.addWidget(self.current_button[2], row2, col2)
                    grid.addWidget(self.sender(), row1, col1)
                    Logic.update_grid(arr_grid)
                self.update_grid()
                grid.update()

            self.current_button = None



    def update_grid(self):
        for i in range(grid.count()):
            item = grid.itemAt(i).widget()
            item.setText(str(arr_grid[i // 8][i % 8]))


app = QApplication(sys.argv)
field = GameField()
sys.exit(app.exec_())
