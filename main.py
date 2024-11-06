import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, 
    QPushButton, QLabel
)
from PyQt6.QtCore import Qt
from model.maze import Maze
from gui.view import MazeView
from controller.controller import MazeController
import re
import glob
from search_algorithm.bfs import BFS
from search_algorithm.dfs_3 import DFS
from search_algorithm.ucs import UCS
from search_algorithm.a_star import A_star

class MainWindow(QWidget):
    def __init__(self):
        self.delete_output_files()

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

        # Horizontal layout for the Start, Reset buttons and Speed selector
        self.button_layout = QHBoxLayout()

        # Button to start the simulation
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_simulation)  # Connect to event handler
        self.button_layout.addWidget(self.start_button)  # Add Start button to button layout

        # Button to reset the simulation
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_simulation)  # Connect to event handler
        self.button_layout.addWidget(self.reset_button)  # Add Reset button to button layout

        # Add Speed ComboBox next to Reset button
        self.speed_selector = QComboBox()
        self.speed_selector.addItems(["x1.0", "x2.0", "x3.0", "x4.0", "x5.0", "x6.0", "x7.0", "x8.0", 
                                      "x9.0", "x10.0", "x12.0", "x15.0", "x18.0", "x20.0", "x25.0", "x30.0",
                                      "x40.0", "x50.0"])  # Add speed options
        self.speed_selector.setCurrentIndex(0)  # Set default selection to "x1.5"
        self.speed_selector.currentTextChanged.connect(self.change_speed)  # Connect to handler
        self.button_layout.addWidget(QLabel("Speed:"))  # Optional label for clarity
        self.button_layout.addWidget(self.speed_selector)  # Add Speed selector to button layout

        # Add the button layout to the main layout
        self.layout.addLayout(self.button_layout)

        self.custom_text = QLabel("Step 0 --- Total cost : 0")  
        self.layout.addWidget(self.custom_text)

        # Initialize maze and its view
        self.current_maze = None
        self.current_view = None

        # Initialize controller
        self.controller = None  # Initialize controller as None

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

            outputs_dir = 'outputs'
            if not os.path.exists(outputs_dir):
                os.makedirs(outputs_dir)  

            print(f"Running {algorithm_name} on {file_path}")

            algorithms = {
                "BFS": BFS,
                "DFS": DFS,
                "UCS": UCS,
                "A*": A_star
            }

            # Run the selected algorithm
            if algorithm_name in algorithms:
                algorithm_class = algorithms[algorithm_name]
                algorithm_instance = algorithm_class(file_path)
                algorithm_instance.run()
                result = algorithm_instance.get_result()

            input_filename = os.path.basename(file_path)
            output_filename = input_filename.replace('input', 'output')
            output_path = os.path.join(outputs_dir, output_filename)

            result.save(output_path, duplicate=False)

            # Stop any existing controller before creating a new one
            if self.controller:
                self.controller.stop()

            self.controller = MazeController(self.current_maze, self.current_view, result, self.custom_text)
            self.controller.finished.connect(self.on_simulation_finished)  # Connect the signal
            
            # Set the initial speed based on the speed selector
            speed_text = self.speed_selector.currentText()
            speed_multiplier = float(speed_text.strip('x'))
            self.controller.set_speed(speed_multiplier)
            
            self.controller.start()  # Start the controller's timer

            self.start_button.setEnabled(False)  # Disable Start button

    def on_simulation_finished(self):
        self.start_button.setEnabled(True)  # Re-enable Start button
        self.controller = None  # Clear the controller reference

    def reset_simulation(self):
        # Stop the controller if it's running
        if self.controller:
            self.controller.stop()
            self.controller = None  # Clear the controller reference
        self.load_maze_from_selected_file(self.file_selector.currentText())
        self.custom_text.setText("Step 0 --- Total cost : 0")
        self.start_button.setEnabled(True)  # Ensure Start button is enabled

    def change_speed(self, text):
        if self.controller:
            try:
                multiplier = float(text.strip('x'))
                self.controller.set_speed(multiplier)
            except ValueError:
                print(f"Invalid speed multiplier selected: {text}")

    def delete_output_files(self):
        outputs_dir = 'outputs'
        pattern = os.path.join(outputs_dir, 'output-*.txt')
        files_to_delete = glob.glob(pattern)
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
