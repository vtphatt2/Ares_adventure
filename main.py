import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton
from model.maze import Maze
from gui.view import MazeView
from controller.controller import MazeController
import re

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ares's Adventure")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # ComboBox to select input file
        self.file_selector = QComboBox()
        self.load_input_files()
        self.file_selector.currentTextChanged.connect(self.load_maze_from_selected_file)
        self.layout.addWidget(self.file_selector)

        # Button to start the simulation
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_simulation)
        self.layout.addWidget(self.start_button)

        # Initialize the maze and view
        self.current_maze = None
        self.current_view = None
        self.load_maze_from_selected_file(self.file_selector.currentText())

    def load_input_files(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        inputs_dir = os.path.join(current_dir, 'inputs')  
        
        files = [
            f for f in os.listdir(inputs_dir)
            if f.endswith(".txt") and self.is_valid_input_file(os.path.join(inputs_dir, f))
        ]
        files = [f for f in os.listdir(inputs_dir) if f.endswith(".txt") and self.is_valid_input_file(os.path.join(inputs_dir, f))]
        files.sort()
        self.file_selector.addItems(files)

    def is_valid_input_file(self, filepath):
        filename = os.path.basename(filepath)
        pattern = r"^input-\d{2}\.txt$" 
        if not re.match(pattern, filename):
            return False 

        try:
            with open(filepath, 'r') as f:
                first_line = f.readline().strip().split()
                list(map(int, first_line))  

                valid_chars = {"#", " ", "$", "@", ".", "*", "+"}
                for line in f:
                    line = line.rstrip('\n')
                    if not all(char in valid_chars for char in line):
                        return False 
                        
            return True  
        except (ValueError, FileNotFoundError):
            return False 

    def load_maze_from_selected_file(self, filename):
        if filename:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            inputs_dir = os.path.join(current_dir, 'inputs')
            filepath = os.path.join(inputs_dir, filename)
            self.current_maze = Maze(filepath)

            if self.current_view:
                self.layout.removeWidget(self.current_view)
                self.current_view.deleteLater()

            self.current_view = MazeView(self.current_maze)
            self.layout.addWidget(self.current_view)

    def start_simulation(self):
        if self.current_maze:
            controller = MazeController(self.current_maze, self.current_view)
            actions = "rrdllu" 
            controller.run_sequence(actions)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
