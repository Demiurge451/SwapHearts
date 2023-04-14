import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        button_labels = [
            ['1', '1', '1', '2'],
            ['3', '2', '2', '3']
        ]

        for row, row_labels in enumerate(button_labels):
            for col, label in enumerate(row_labels):
                button = QPushButton(label)
                button.setFixedSize(50, 50)
                button.clicked.connect(lambda checked, row=row, col=col: self.onButtonClicked(row, col))
                grid.addWidget(button, row, col)

        self.current_button = None

        self.setLayout(grid)
        self.setWindowTitle('Grid Example')
        self.show()

    def onButtonClicked(self, row, col):
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
                grid.addWidget(self.current_button[2], row2, col2)
                grid.addWidget(self.sender(), row1, col1)
            self.current_button = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec_())