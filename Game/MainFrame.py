import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
import Logic
from random import randint

arr_grid = [[randint(1, 6) for j in range(8)] for i in range(8)]


# TODO add diapason
class GameField(QWidget):
    def __init__(self):
        super().__init__()


        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        Logic.update_grid(arr_grid)
        button_labels = [[str(i) for i in j] for j in arr_grid]
        for row, row_labels in enumerate(button_labels):
            for col, label in enumerate(row_labels):
                button = QPushButton(label)
                button.setFixedSize(50, 50)
                button.clicked.connect(lambda checked, row=row, col=col: self.onButtonClicked(row, col))
                grid.addWidget(button, row, col)

        self.current_button = None

        self.setLayout(grid)
        self.setGeometry(100, 100, 300, 300)
        self.show()

    def on_button_clicked(self, button):
        if self.current_button is None:
            # First button clicked
            self.current_button = button
        else:
            # Second button clicked - swap buttons
            grid = self.layout()
            pos1 = grid.indexOf(self.current_button)
            pos2 = grid.indexOf(button)
            row1, col1, _, _ = grid.getItemPosition(pos1)
            row2, col2, _, _ = grid.getItemPosition(pos2)
            grid.addWidget(button, row1, col1)
            grid.addWidget(self.current_button, row2, col2)
            self.current_button = None


app = QApplication(sys.argv)
field = GameField()
sys.exit(app.exec_())
