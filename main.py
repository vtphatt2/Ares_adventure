import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, 
    QPushButton, QLabel, QDialog, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from model.maze import Maze
from gui.view import MazeView
from controller.controller import MazeController
import re
import glob
from search_algorithm.bfs import BFS
from search_algorithm.dfs_3 import DFS
from search_algorithm.ucs_new import UCS
from search_algorithm.a_star import A_star

class SolverThread(QThread):
    finished = pyqtSignal(object)
    
    def __init__(self, algorithm_class, file_path):
        super().__init__()
        self.algorithm_class = algorithm_class
        self.file_path = file_path

    def run(self):
        algorithm_instance = self.algorithm_class(self.file_path)
        algorithm_instance.run()
        result = algorithm_instance.get_result()
        self.finished.emit(result)

class RunningDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Solver Running")
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        layout = QVBoxLayout()
        label = QLabel("Solver is running. Please wait...")
        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ares's Adventure")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.top_layout = QHBoxLayout()

        self.file_selector = QComboBox()
        self.load_input_files()
        self.file_selector.currentTextChanged.connect(self.load_maze_from_selected_file)
        self.top_layout.addWidget(self.file_selector)

        self.algorithm_selector = QComboBox()
        self.algorithm_selector.addItems(["BFS", "DFS", "UCS", "A*"])
        self.top_layout.addWidget(self.algorithm_selector)

        self.layout.addLayout(self.top_layout)

        self.button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_simulation)
        self.button_layout.addWidget(self.start_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_simulation)
        self.button_layout.addWidget(self.reset_button)

        self.speed_selector = QComboBox()
        self.speed_selector.addItems(["x1.0", "x2.0", "x3.0", "x4.0", "x5.0", "x6.0", "x7.0", "x8.0", 
                                      "x9.0", "x10.0", "x12.0", "x15.0", "x18.0", "x20.0", "x25.0", "x30.0",
                                      "x40.0", "x50.0"])
        self.speed_selector.setCurrentIndex(0)
        self.speed_selector.currentTextChanged.connect(self.change_speed)
        self.button_layout.addWidget(QLabel("Speed:"))
        self.button_layout.addWidget(self.speed_selector)

        self.layout.addLayout(self.button_layout)

        self.custom_text = QLabel("Step 0 --- Total cost : 0")  
        self.layout.addWidget(self.custom_text)

        self.current_maze = None
        self.current_view = None
        self.controller = None
        self.thread = None
        self.dialog = None

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

            if algorithm_name in algorithms:
                algorithm_class = algorithms[algorithm_name]
                
                self.dialog = RunningDialog(self)
                self.dialog.show()

                self.thread = SolverThread(algorithm_class, file_path)
                self.thread.finished.connect(self.on_solver_finished)
                self.thread.start()

                self.start_button.setEnabled(False)

    def on_solver_finished(self, result):
        input_filename = os.path.basename(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'inputs', self.file_selector.currentText()))
        output_filename = input_filename.replace('input', 'output')
        output_path = os.path.join('outputs', output_filename)

        result.save(output_path, duplicate=True)

        if self.controller:
            self.controller.stop()

        self.controller = MazeController(self.current_maze, self.current_view, result, self.custom_text)
        self.controller.finished.connect(self.on_simulation_finished)

        speed_text = self.speed_selector.currentText()
        speed_multiplier = float(speed_text.strip('x'))
        self.controller.set_speed(speed_multiplier)
        
        self.controller.start()

        self.dialog.close()
        self.thread = None

    def on_simulation_finished(self):
        self.start_button.setEnabled(True)
        self.controller = None

    def reset_simulation(self):
        if self.controller:
            self.controller.stop()
            self.controller = None
        self.load_maze_from_selected_file(self.file_selector.currentText())
        self.custom_text.setText("Step 0 --- Total cost : 0")
        self.start_button.setEnabled(True)

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
