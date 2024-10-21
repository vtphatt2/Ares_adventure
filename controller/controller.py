from PyQt6.QtCore import QTimer

class MazeController:
    def __init__(self, maze, view, result):
        self.maze = maze
        self.view = view
        self.result = result
        self.ares_position = maze.get_start_position()
        self.step_index = 0

    def move_ares(self, action):
        x, y = self.ares_position
        dx, dy = 0, 0
        if action == 'u': dx, dy = -1, 0
        elif action == 'd': dx, dy = 1, 0
        elif action == 'l': dx, dy = 0, -1
        elif action == 'r': dx, dy = 0, 1

        new_x, new_y = x + dx, y + dy
        if self.maze.grid[new_x][new_y] == ' ':
            self.maze.update_position(x, y, ' ')
            self.maze.update_position(new_x, new_y, '@')
            self.ares_position = (new_x, new_y)
            self.view.draw_maze()

    def run_sequence(self):
        if self.step_index < len(self.result.sequence_of_actions):
            action = self.result.sequence_of_actions[self.step_index]
            self.move_ares(action)
            self.step_index += 1
            QTimer.singleShot(500, self.run_sequence)
