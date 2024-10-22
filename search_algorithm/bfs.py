import time
from collections import deque
import psutil
from model.result import Result

def get_start_state(input_file = ""):
    if input_file == "":
        return -1

    with open(input_file, "r") as f:
        lines = f.readlines()

    maze = []           # 2D list representing the maze
    ares_position = None
    stone_positions = []
    switch_positions = []
    
    # Parse the file line by line
    for i, line in enumerate(lines):
        row = []  # To store the current row of the maze
        for j, char in enumerate(line.strip()):
            if char == '@':  # Ares' position
                ares_position = (i, j)
                row.append(' ')  # Ares is movable -> free space
            elif char == '$':  # Stone position
                stone_positions.append((i, j))
                row.append(' ')  # Stones are considered as movable objects -> free space
            elif char == '.':  # Switch position
                switch_positions.append((i, j))
                row.append('.') 
            elif char == '#':  # Wall
                row.append('#') 
            else:
                row.append(' ') 
        maze.append(row)  # Add the row to the maze

    return {
        'ares': ares_position,
        'stones': stone_positions,
        'switches': switch_positions,
        'maze': maze
    }

class BFS:
    def __init__(self, input_file = ""):
        self.input_file = input_file
        self.result = Result(search_algo_name = "BFS")
        self.start_state = get_start_state(input_file)

    def get_result(self):
        return self.result
    
    def run(self):
        #TODO: Count the total weight he has to push
        if self.start_state == -1:
            #TODO: Notify for user that the input file is not found
            return
        # Start timing
        start_time = time.time()
        start_state = (self.start_state['ares'], tuple(self.start_state['stones']))
        queue = deque([start_state])
        visited = set([start_state])
        parent_map = {start_state: None}
        nodes_generated = 0

        while queue:
            current_state = queue.popleft()
            ares_position, stone_positions = current_state
            nodes_generated += 1

            if all(stone in self.start_state['switches'] for stone in stone_positions):
                path = self.reconstruct_path(current_state, parent_map)
                self.result.set_sequence_of_actions(path)
                self.result.set_steps(len(path))
                break
                
            for neighbor_state, action in self.get_neighbors(current_state):
                if neighbor_state not in visited:
                    visited.add(neighbor_state)
                    queue.append(neighbor_state)
                    parent_map[neighbor_state] = (current_state, action)
                    
        # End timing
        end_time = time.time()
        # Convert to milliseconds
        elapsed_time_ms = (end_time - start_time) * 1000  
        self.result.set_time(elapsed_time_ms)
        self.result.set_memory(self.calculate_memory())

    def get_neighbors(self, state):
        neighbors = []
        ares_position, stone_positions = state
        directions = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
        for action, (dx, dy) in directions.items():
            new_ares_position = (ares_position[0] + dx, ares_position[1] + dy)
            if self.is_free_move(new_ares_position, stone_positions):
                new_state = (new_ares_position, stone_positions)
                neighbors.append((new_state, action))
            # Check if the stone can be pushed
            if new_ares_position in stone_positions:
                stone_index = stone_positions.index(new_ares_position)
                new_stone_position = (new_ares_position[0] + dx, new_ares_position[1] + dy)
                if self.is_valid_move(new_stone_position, stone_positions):
                    new_stone_positions = list(stone_positions)
                    new_stone_positions[stone_index] = new_stone_position
                    new_state = (new_ares_position, tuple(new_stone_positions))
                    neighbors.append((new_state, action))
        return neighbors
    
    def is_valid_move(self, position, stone_positions):
        x, y = position
        if self.start_state['maze'][x][y] == '#': # prevent b case
            return False
        if position in stone_positions: # prevent c case
            return False
        return True

    def reconstruct_path(self, state, parent_map):
        path = []
        current_state = state
        while parent_map[current_state] is not None:
            current_state, action = parent_map[current_state]
            path.append(action)
        # The path is constructed in reverse (from goal to start), path[::-1] reverse it at the end
        return path[::-1]
             
    def calculate_memory(self):
        process = psutil.Process()
        memory_info = process.memory_info()
        return memory_info.rss  # Resident Set Size: the non-swapped physical memory the process has used
