import heapq
import time
import sys
from model.result import Result


class MazeState:
    def __init__(self, maze, player_pos, stone_positions, parent=None, action=None, path_cost=0, cost_steps=None):
        self.maze = maze
        self.player_pos = player_pos
        self.stone_positions = stone_positions
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.cost_steps = cost_steps or []

    def __lt__(self, other):
        return self.path_cost < other.path_cost


class UCS:
    def __init__(self, input_file=""):
        self.input_file = input_file
        self.result = Result(search_algo_name="UCS")

    def read_input(self, filename):
        with open(filename, 'r') as file:
            stone_weights = list(map(int, file.readline().strip().split()))
            maze = [list(line) for line in file]
        return stone_weights, maze

    def find_player_and_stones(self, maze):
        player_pos = None
        stone_positions = []
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell in '@+':
                    player_pos = (y, x)
                elif cell in '$*':
                    stone_positions.append((y, x))
        return player_pos, stone_positions

    def is_goal(self, state):
        return all(state.maze[y][x] in '*+' for y, x in state.stone_positions)

    def is_deadlock(self, state):
        def is_corner_deadlock(stone_position, maze):
            y, x = stone_position
            if maze[y][x] == '*':  # Stone on goal
                return False
            return (maze[y - 1][x] == '#' and maze[y][x - 1] == '#') or \
                (maze[y - 1][x] == '#' and maze[y][x + 1] == '#') or \
                (maze[y + 1][x] == '#' and maze[y][x - 1] == '#') or \
                (maze[y + 1][x] == '#' and maze[y][x + 1] == '#')

        def is_wall_deadlock(stone_position, maze):
            y, x = stone_position
            if maze[y][x] == '*':  # Stone on goal
                return False

            height = len(maze)
            width = len(maze[0])

            # Horizontal wall check (left or right wall)
            if x == 0 or x == width - 1:
                has_goal_in_row = any(maze[y][i] == '.' for i in range(width))
                return not has_goal_in_row

            # Vertical wall check (top or bottom wall)
            if y == 0 or y == height - 1:
                has_goal_in_column = any(maze[i][x] == '.' for i in range(height))
                return not has_goal_in_column

            return False

        for stone in state.stone_positions:
            if is_corner_deadlock(stone, state.maze) or is_wall_deadlock(stone, state.maze):
                return True
        return False

    def get_neighbors(self, state, stone_weights):
        neighbors = []
        directions = [('U', -1, 0), ('D', 1, 0), ('L', 0, -1), ('R', 0, 1)]

        for action, dy, dx in directions:
            new_y, new_x = state.player_pos[0] + dy, state.player_pos[1] + dx
            if state.maze[new_y][new_x] in ' .':
                new_maze = [row[:] for row in state.maze]
                new_maze[state.player_pos[0]][state.player_pos[1]] = ' ' if state.maze[state.player_pos[0]][
                                                                                state.player_pos[1]] == '@' else '.'
                new_maze[new_y][new_x] = '@' if new_maze[new_y][new_x] == ' ' else '+'

                new_cost_steps = state.cost_steps[:]
                new_cost_steps.append(state.path_cost + 1)

                new_state = MazeState(new_maze, (new_y, new_x), state.stone_positions, state, action.lower(),
                                      state.path_cost + 1, new_cost_steps)
                neighbors.append(new_state)
            elif state.maze[new_y][new_x] in '$*':
                stone_index = state.stone_positions.index((new_y, new_x))
                new_stone_y, new_stone_x = new_y + dy, new_x + dx
                if state.maze[new_stone_y][new_stone_x] in ' .':
                    new_maze = [row[:] for row in state.maze]
                    new_maze[state.player_pos[0]][state.player_pos[1]] = ' ' if state.maze[state.player_pos[0]][
                                                                                    state.player_pos[1]] == '@' else '.'
                    new_maze[new_y][new_x] = '@' if new_maze[new_y][new_x] == '$' else '+'
                    new_maze[new_stone_y][new_stone_x] = '$' if new_maze[new_stone_y][new_stone_x] == ' ' else '*'
                    new_stone_positions = state.stone_positions[:]
                    new_stone_positions[stone_index] = (new_stone_y, new_stone_x)

                    new_cost_steps = state.cost_steps[:]
                    new_cost_steps.append(state.path_cost + stone_weights[stone_index] + 1)

                    new_state = MazeState(new_maze, (new_y, new_x), new_stone_positions, state, action,
                                          state.path_cost + stone_weights[stone_index] + 1, new_cost_steps)
                    neighbors.append(new_state)

        return neighbors

    def ucs(self, initial_state, stone_weights):
        frontier = [(0, initial_state)]
        explored = set()
        nodes_visited = 0
        max_frontier_size = 0

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            _, current_state = heapq.heappop(frontier)

            if self.is_goal(current_state):
                path = []
                state = current_state
                while state.parent:
                    path.append(state.action)
                    state = state.parent
                return path[::-1], nodes_visited, current_state.path_cost, current_state.cost_steps, max_frontier_size

            state_hash = (current_state.player_pos, tuple(current_state.stone_positions))
            if state_hash in explored:
                continue

            explored.add(state_hash)
            nodes_visited += 1

            for neighbor in self.get_neighbors(current_state, stone_weights):
                if not self.is_deadlock(neighbor):  # Skip deadlock states
                    heapq.heappush(frontier, (neighbor.path_cost, neighbor))

        return None, nodes_visited, 0, [], max_frontier_size

    def run(self):
        start_time = time.time()
        start_memory = sys.getsizeof(globals()) + sys.getsizeof(locals())

        stone_weights, maze = self.read_input(self.input_file)
        player_pos, stone_positions = self.find_player_and_stones(maze)
        initial_state = MazeState(maze, player_pos, stone_positions)

        path, nodes_visited, total_cost, cost_steps, max_frontier_size = self.ucs(initial_state, stone_weights)

        end_time = time.time()
        end_memory = sys.getsizeof(globals()) + sys.getsizeof(locals())

        if path:
            self.result.set_steps(len(path))
            self.result.set_sequence_of_actions(''.join(path))
            self.result.set_node(nodes_visited)
            self.result.set_total_cost(total_cost)
            self.result.set_cost_steps(cost_steps)
        else:
            print("No solution found.")

        self.result.set_time((end_time - start_time) * 1000)  # Convert to milliseconds
        self.result.set_memory((end_memory - start_memory) / (1024 * 1024))  # Convert to MB
        self.result.save("ucs_result.txt")

    def get_result(self):
        return self.result
