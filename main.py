import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton, QLabel
from model.maze import Maze
from gui.view import MazeView
from controller.controller import MazeController
import re
from search_algorithm.bfs import BFS
from search_algorithm.dfs import DFS
from search_algorithm.ucs import UCS
from search_algorithm.a_star import A_star

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

        # Horizontal layout for the Start and Reset buttons
        self.button_layout = QHBoxLayout()

        # Button to start the simulation
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_simulation)  # Connect to event handler
        self.button_layout.addWidget(self.start_button)  # Add Start button to button layout

        # Button to reset the simulation
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_simulation)  # Connect to event handler
        self.button_layout.addWidget(self.reset_button)  # Add Reset button to button layout

        # Add the button layout to the main layout
        self.layout.addLayout(self.button_layout)

        self.custom_text = QLabel("Step 0 --- Total cost : 0")  
        self.layout.addWidget(self.custom_text)

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

            if algorithm_name == "BFS":
                bfs = BFS(file_path)
                bfs.run()
                result = bfs.get_result()
            elif algorithm_name == "DFS":
                dfs = DFS(file_path)
                dfs.run()
                result = dfs.get_result()
            elif algorithm_name == "UCS":
                ucs = UCS(file_path)
                ucs.run()
                result = ucs.get_result()
            elif algorithm_name == "A*":
                a_star = A_star(file_path)
                a_star.run()
                result = a_star.get_result()

            self.controller = MazeController(self.current_maze, self.current_view, result, self.custom_text)
            self.controller.run_sequence()

    def reset_simulation(self):
        self.load_maze_from_selected_file(self.file_selector.currentText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
