import sys
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QApplication
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap

class MazeView(QWidget):
    # Window size
    WINDOW_WIDTH = 1300
    WINDOW_HEIGHT = 650

    # Color
    OUTER_WALL_COLOR = "#8B4513"  # saddlebrown
    INNER_CELL_COLOR = "transparent"
    BORDER_COLOR = "black"

    def __init__(self, maze):
        super().__init__()
        self.maze = maze
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ares's Adventure")
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setStyleSheet("background-color: white;")

        self.rows = len(self.maze.grid)
        self.cols = len(self.maze.grid[0])
        self.calculate_cell_size()

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        maze_widget = QWidget()
        maze_width = self.cols * self.CELL_SIZE
        maze_height = self.rows * self.CELL_SIZE
        maze_widget.setLayout(self.grid_layout)
        maze_widget.setFixedSize(maze_width, maze_height)

        main_h_layout = QHBoxLayout()
        main_h_layout.addStretch()
        main_h_layout.addWidget(maze_widget)
        main_h_layout.addStretch()
        main_v_layout = QVBoxLayout()
        main_v_layout.addStretch()
        main_v_layout.addLayout(main_h_layout)
        main_v_layout.addStretch()

        self.setLayout(main_v_layout)
        self.draw_maze()

    def calculate_cell_size(self):
        calculated_size_width = self.WINDOW_WIDTH / self.cols - 10
        calculated_size_height = self.WINDOW_HEIGHT / self.rows - 10
        self.CELL_SIZE = int(min(calculated_size_width, calculated_size_height))
        self.CELL_SIZE = max(self.CELL_SIZE, 10)

    def draw_maze(self):
        for i, row in enumerate(self.maze.grid):
            for j, cell in enumerate(row):
                widget = self.get_widget_for_cell(cell, i, j)
                self.grid_layout.addWidget(widget, i, j)

    def get_widget_for_cell(self, cell, row, col):
        if cell == '#':
            return self.create_wall_cell(row, col)
        elif cell == ' ':
            return self.create_empty_cell(row, col)
        elif cell == '@':
            return self.create_character_cell(row, col)
        elif cell == '$':
            return self.create_rock_cell(row, col, weight=self.maze.stone_weights.pop(0))
        elif cell == '.':
            return self.create_switch_cell(row, col)
        elif cell == '*':
            return self.create_rock_on_switch_cell(row, col)
        elif cell == '+':
            return self.create_character_on_switch_cell(row, col)
        else:
            return self.create_empty_cell(row, col)

    def _get_border_style(self, row, col):
        top = "1px solid black" if row == 0 else "0px"
        left = "1px solid black" if col == 0 else "0px"
        right = "1px solid black" if col < self.cols - 1 else "0px"
        bottom = "1px solid black" if row < self.rows - 1 else "0px"

        return (
            f"border-top: {top}; "
            f"border-left: {left}; "
            f"border-right: {right}; "
            f"border-bottom: {bottom};"
        )

    def create_wall_cell(self, row, col):
        frame = QFrame()
        frame.setFixedSize(self.CELL_SIZE, self.CELL_SIZE)
        style = self._get_border_style(row, col)
        frame.setStyleSheet(f"background-color: {self.OUTER_WALL_COLOR}; {style}")
        return frame

    def create_empty_cell(self, row, col):
        frame = QFrame()
        frame.setFixedSize(self.CELL_SIZE, self.CELL_SIZE)
        style = self._get_border_style(row, col)
        frame.setStyleSheet(f"background-color: {self.INNER_CELL_COLOR}; {style}")
        return frame

    def create_character_cell(self, row, col):
        return self._create_image_frame("images/ares.jpg", row, col, scale_factor=1.2)

    def create_rock_cell(self, row, col, weight):
        return self._create_rock_image_frame("images/rock.svg", row, col, scale_factor=1, weight=weight)

    def create_switch_cell(self, row, col):
        return self._create_image_frame("images/switch.svg", row, col, scale_factor=0.6)

    def create_rock_on_switch_cell(self, row, col):
        frame = QFrame()
        frame.setFixedSize(self.CELL_SIZE, self.CELL_SIZE)
        style = self._get_border_style(row, col)
        frame.setStyleSheet(f"background-color: transparent; {style}")

        label = QLabel('*', frame)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: red; font-weight: bold; font-size: 20px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(-5, -5, -5, -5)
        layout.addWidget(label)
        frame.setLayout(layout)

        return frame

    def create_character_on_switch_cell(self, row, col):
        frame = QFrame()
        frame.setFixedSize(self.CELL_SIZE, self.CELL_SIZE)
        style = self._get_border_style(row, col)
        frame.setStyleSheet(f"background-color: transparent; {style}")

        label = QLabel('+', frame)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: blue; font-weight: bold; font-size: 20px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(-5, -5, -5, -5)
        layout.addWidget(label)
        frame.setLayout(layout)

        return frame

    def _create_rock_image_frame(self, image_path, row, col, scale_factor=1.0, weight=100):
        frame = QFrame()
        frame.setFixedSize(self.CELL_SIZE, self.CELL_SIZE)
        style = self._get_border_style(row, col)
        frame.setStyleSheet(f"background-color: {self.INNER_CELL_COLOR}; {style}")

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        frame.setLayout(layout)

        image_label = QLabel(frame)
        pixmap = QPixmap(image_path)

        new_width = int(self.CELL_SIZE * scale_factor)
        new_height = int(self.CELL_SIZE * scale_factor)

        pixmap = pixmap.scaled(
            new_width, new_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("border: none; background-color: transparent;")

        layout.addWidget(image_label, 0, 0)

        weight_label = QLabel(str(weight), frame)
        weight_size = 36  
        weight_label.setFixedSize(QSize(weight_size, weight_size))
        weight_label.setStyleSheet("""
            color: white;
            background-color: rgba(1, 1, 1, 1);
            border-radius: 18px;
            padding: 2px 5px;
            font-weight: bold;
        """)
        weight_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(weight_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

        return frame

    def _create_image_frame(self, image_path, row, col, scale_factor=1.0):
        frame = QFrame()
        frame.setFixedSize(self.CELL_SIZE, self.CELL_SIZE)
        style = self._get_border_style(row, col)
        frame.setStyleSheet(f"background-color: {self.INNER_CELL_COLOR}; {style}")

        label = QLabel(frame)
        pixmap = QPixmap(image_path)

        new_width = int(self.CELL_SIZE * scale_factor)
        new_height = int(self.CELL_SIZE * scale_factor)

        pixmap = pixmap.scaled(
            new_width, new_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("border: none; background-color: transparent;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label)
        frame.setLayout(layout)

        return frame

