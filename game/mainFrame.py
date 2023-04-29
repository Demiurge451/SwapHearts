import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QToolBar, QLabel, \
    QSizePolicy, QHBoxLayout

from game.gameField import GameField
from game.instruction import InstructionsWindow
from game.settings import SettingsWindow


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
        layout = QVBoxLayout()
        self.field = GameField()
        self.field.score_changed.connect(self.score_label.update_score)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(layout)

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
        self.new_game_button = MyButton("New game")
        self.new_game_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.new_game_button.setMaximumSize(200, 50)

        self.new_game_button.clicked.connect(self.start_new_game)

        header.addWidget(self.new_game_button)
        header.addStretch()
        header.addWidget(self.score_label)
        layout.addLayout(header)
        layout.addWidget(self.field)

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
