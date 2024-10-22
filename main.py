import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton
from model.maze import Maze
from model.result import Result
from gui.view import MazeView
from controller.controller import MazeController
import re

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ares's Adventure")  # Set the window title

        # Main vertical layout for the window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Horizontal layout for the file selector and algorithm selector
        self.top_layout = QHBoxLayout()

        # ComboBox for selecting the input file
        self.file_selector = QComboBox()
        self.load_input_files()  # Load available input files into the ComboBox
        self.file_selector.currentTextChanged.connect(self.load_maze_from_selected_file)  
        self.top_layout.addWidget(self.file_selector)  # Add to horizontal layout

        # ComboBox for selecting the algorithm
        self.algorithm_selector = QComboBox()
        self.algorithm_selector.addItems(["BFS", "DFS", "UCS", "A*"])  # Add options
        self.top_layout.addWidget(self.algorithm_selector)  # Add to horizontal layout

        # Add the horizontal layout to the main vertical layout
        self.layout.addLayout(self.top_layout)

        # Button to start the simulation
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_simulation)  # Connect to event handler
        self.layout.addWidget(self.start_button)  # Add button to the main layout

        # Initialize maze and its view
        self.current_maze = None
        self.current_view = None

        # Load the default maze from the currently selected file
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
            algorithm_name = self.algorithm_selector.currentText()
            current_dir = os.path.dirname(os.path.realpath(__file__))  
            inputs_dir = os.path.join(current_dir, 'inputs')  
            file_name = self.file_selector.currentText()  
            file_path = os.path.join(inputs_dir, file_name)  

            print(f"Running {algorithm_name} on {file_path}")

            # result = Result("BFS", 5, 30, 300, 30.0, 30.0, "uLulDrrRRRRR")  # fake result
            # self.controller = MazeController(self.current_maze, self.current_view, result)
            # self.controller.run_sequence()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
