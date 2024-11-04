import time
from collections import deque
from model.memory import MemoryTracker
from model.result import Result

class DFS:
    def __init__(self, input_file=""):
        self.input_file = input_file
        self.result = Result(search_algo_name="DFS")
        self.start_state = self.get_start_state(input_file)

    def get_start_state(self, input_file=""):
        if input_file == "":
            raise ValueError("No input file provided.")
            return -1

        with open(input_file, "r") as f:
            lines = f.readlines()

        maze = []           # 2D list representing the maze
        ares_position = None
        stone_positions = []
        stone_weights = []
        switch_positions = []

        # Parse the file line by line
        for i, line in enumerate(lines):
            if i == 0:  # First line contains stone weights
                stone_weights = list(map(int, line.strip().split()))
                continue
            row = []  # To store the current row of the maze
            for j, char in enumerate(line.strip()):
                if char == '@':  # Ares' position
                    ares_position = (j, i - 1)
                    row.append(' ')  # Ares is movable -> free space
                elif char == '*': 
                    stone_positions.append((j, i - 1))
                    switch_positions.append((j, i - 1))
                elif char == '$':  # Stone position
                    stone_positions.append((j, i - 1))
                    row.append(' ')  # Stones are considered as movable objects -> free space
                elif char == '.':  # Switch position
                    switch_positions.append((j, i - 1))
                    row.append('.') 
                elif char == '#':  # Wall
                    row.append('#') 
                else:
                    row.append(' ') 
            maze.append(row)  # Add the row to the maze

        # Ensure the number of weights matches the number of stones
        if len(stone_weights) != len(stone_positions):
            raise ValueError("Number of stone weights does not match the number of stones.")

        return {
            'ares': ares_position,
            'stones': stone_positions,
            'stone_weights': stone_weights,
            'switches': switch_positions,
            'maze': tuple(maze),
            'cost': 0
        }

    def get_result(self):
        return self.result
    
    def run(self):
        if self.start_state == -1:
            return
    
        start_time = time.time()
        memory_tracker = MemoryTracker()

        start_state = (self.start_state['ares'], tuple(self.start_state['stones']))
        stack = [start_state]
        visited = set([start_state])
        parent_map = {start_state: None}
        nodes_generated = 0

        while stack:
            current_state = stack.pop()
            ares_position, stone_positions = current_state
            nodes_generated += 1

            if all(stone in self.start_state['switches'] for stone in stone_positions):
                print("Goal reached!")
                path = self.reconstruct_path(current_state, parent_map)
                self.result.set_sequence_of_actions(path)
                self.result.set_steps(len(path))
                self.result.set_cost_steps(self.find_cost_each_step(path))
                total_cost = self.result.get_cost_steps()[-1]
                self.result.set_total_cost(total_cost)
                break

            for neighbor_state, action in self.get_neighbors(current_state):
                if neighbor_state not in visited:
                    visited.add(neighbor_state)
                    stack.append(neighbor_state)
                    parent_map[neighbor_state] = (current_state, action)

        end_time = time.time()

        self.result.set_time((end_time - start_time) * 1000)
        self.result.set_memory(memory_tracker.peak_memory_usage()) 
        self.result.set_node(nodes_generated)

        memory_tracker.stop_tracking()

    def get_neighbors(self, state):
        neighbors = []
        ares_position, stone_positions = state
        directions = {'u': (0, -1), 'l': (-1, 0), 'd': (0, 1), 'r': (1, 0)}
        for action, (dx, dy) in directions.items():
            new_ares_position = (ares_position[0] + dx, ares_position[1] + dy)
            # Move Ares without pushing a stone
            if self.is_valid_move(new_ares_position, stone_positions):
                new_state = (new_ares_position, stone_positions)
                neighbors.append((new_state, action))
            # Check if the stone can be pushed
            elif new_ares_position in stone_positions:
                stone_index = stone_positions.index(new_ares_position)
                new_stone_position = (new_ares_position[0] + dx, new_ares_position[1] + dy)

                if self.is_valid_move(new_stone_position, stone_positions):
                    new_stone_positions = list(stone_positions)
                    new_stone_positions[stone_index] = new_stone_position
                    new_state = (new_ares_position, tuple(new_stone_positions))
                    neighbors.append((new_state, action.upper()))

        return neighbors

    def is_valid_move(self, position, stone_positions):
        x, y = position
        if self.start_state['maze'][y][x] == '#': # Prevent moving into wall
            return False
        if position in stone_positions: # Prevent pushing a stone into another stone
            return False
        return True

    def reconstruct_path(self, state, parent_map):
        path = []
        current_state = state
        while parent_map[current_state] is not None:
            current_state, action = parent_map[current_state]
            path.append(action)
        # The path is constructed in reverse (from goal to start), path[::-1] reverse it at the end
        return ''.join(path[::-1])

    def find_cost_each_step(self, path):
        total_cost = 0
        ares_position = self.start_state['ares']
        stone_positions = list(self.start_state['stones'])  # Mutable list of stone positions
        cost_each_step = []
        
        directions = {'u': (0, -1), 'l': (-1, 0), 'd': (0, 1), 'r': (1, 0)}
        
        for action in path:
            if action.islower():  # Regular move
                dx, dy = directions[action]
                ares_position = (ares_position[0] + dx, ares_position[1] + dy)
                total_cost += 1  # Each move costs 1
            
            else:  # Stone push
                direction = action.lower()  # Push in the same direction, but action is uppercase
                dx, dy = directions[direction]
                new_ares_position = (ares_position[0] + dx, ares_position[1] + dy)
                
                # Find which stone is being pushed
                for i, stone_pos in enumerate(stone_positions):
                    if stone_pos == new_ares_position:  # Stone is pushed by Ares
                        new_stone_position = (stone_pos[0] + dx, stone_pos[1] + dy)
                        stone_positions[i] = new_stone_position  
                        stone_weight = self.start_state['stone_weights'][i]
                        total_cost += (1 + stone_weight)  # Pushing a stone costs 1 + stone weight
                        break
                
                # Ares also moves to the stone's previous position
                ares_position = new_ares_position

            cost_each_step.append(total_cost)

        return cost_each_step
    