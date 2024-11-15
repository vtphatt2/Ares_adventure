from PyQt6.QtCore import QTimer, QObject, pyqtSignal

class MazeController(QObject):
    finished = pyqtSignal()

    def __init__(self, maze, view, result, label):  
        super().__init__()  # Initialize QObject
        self.maze = maze
        self.view = view
        self.result = result
        self.label = label
        self.ares_position = maze.get_start_position()
        self.step_index = 0
        
        self.base_interval = 500  
        self.speed_multiplier = 1.0 

        self.timer = QTimer()
        self.timer.setInterval(int(self.base_interval / self.speed_multiplier))  
        self.timer.timeout.connect(self.run_sequence)

    def move_ares(self, action):
        if not self.ares_position:
            return

        direction, push = self.parse_action(action)
        if not direction:
            print(f"The action '{action}' is invalid.")
            return

        dx, dy = direction
        x, y = self.ares_position
        target_x, target_y = x + dx, y + dy

        if self.maze.grid[target_x][target_y] == '#':
            print("Cannot move into a wall.")
            return

        if self.maze.grid[target_x][target_y] in {'$', '*'}:
            if not push:
                print("A stone is blocking the way. Use a push action to move it.")
                return

            new_stone_x, new_stone_y = target_x + dx, target_y + dy

            if self.maze.grid[new_stone_x][new_stone_y] in {' ', '.'}:
                self.update_cell(target_x, target_y, new_stone_x, new_stone_y)
                self.update_ares_position(x, y, target_x, target_y)
            else:
                print("Cannot push the stone into this position.")
                return
        elif self.maze.grid[target_x][target_y] in {' ', '.'}:
            self.update_ares_position(x, y, target_x, target_y)
        else:
            print(f"The target cell '{self.maze.grid[target_x][target_y]}' is invalid.")
            return

        self.ares_position = (target_x, target_y)
        self.view.draw_maze()

    def parse_action(self, action):
        actions = {
            'u': (-1, 0),
            'd': (1, 0),
            'l': (0, -1),
            'r': (0, 1),
            'U': (-1, 0),
            'D': (1, 0),
            'L': (0, -1),
            'R': (0, 1),
        }
        if action not in actions:
            return None, False
        direction = actions[action]
        push = action.isupper()
        return direction, push

    def update_cell(self, stone_x, stone_y, new_stone_x, new_stone_y):
        stone_on_switch = self.maze.grid[stone_x][stone_y] == '*'
        weight = self.maze.stones.get((stone_x, stone_y), 100)

        if (stone_x, stone_y) in self.maze.stones:
            del self.maze.stones[(stone_x, stone_y)]

        if self.maze.grid[new_stone_x][new_stone_y] == '.':
            self.maze.grid[new_stone_x][new_stone_y] = '*'
        else:
            self.maze.grid[new_stone_x][new_stone_y] = '$'

        self.maze.stones[(new_stone_x, new_stone_y)] = weight

        if stone_on_switch:
            self.maze.grid[stone_x][stone_y] = '.'
        else:
            self.maze.grid[stone_x][stone_y] = ' '

    def update_ares_position(self, old_x, old_y, new_x, new_y):
        ares_on_switch = (self.maze.grid[old_x][old_y] == '+')

        if ares_on_switch:
            self.maze.grid[old_x][old_y] = '.'
        else:
            self.maze.grid[old_x][old_y] = ' '

        if self.maze.grid[new_x][new_y] == '.':
            self.maze.grid[new_x][new_y] = '+'
        else:
            self.maze.grid[new_x][new_y] = '@'

    def run_sequence(self):
            if self.step_index < len(self.result.sequence_of_actions):
                action = self.result.sequence_of_actions[self.step_index]
                print(f"Executing action: {action}")
                for row in self.maze.grid:
                    print(row)
                self.move_ares(action)

                total_cost = self.result.get_cost_steps()[self.step_index]
                self.label.setText(f"Step {self.step_index + 1} --- Total cost: {total_cost}")

                self.step_index += 1
            else:
                self.timer.stop()  # Stop the timer when done

    def start(self):
        self.timer.start()

    def stop(self):
        if self.timer.isActive():
            self.timer.stop()
            self.finished.emit()
    
    def set_speed(self, multiplier):
        if multiplier <= 0:
            print("Speed multiplier must be positive.")
            return
        self.speed_multiplier = multiplier
        new_interval = int(self.base_interval / self.speed_multiplier)
        self.timer.setInterval(new_interval)
        print(f"Speed set to x{self.speed_multiplier}, Timer interval adjusted to {new_interval} ms.")

