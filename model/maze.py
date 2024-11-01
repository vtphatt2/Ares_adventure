class Maze:
    def __init__(self, filepath):
        self.grid = []
        self.stone_weights = []
        self.stones = {}
        self.load_maze(filepath)

    def load_maze(self, filepath):
        with open(filepath, 'r') as f:
            weight_line = f.readline().strip()
            self.stone_weights = list(map(int, weight_line.split()))
            raw_grid = [line.rstrip('\n') for line in f]

        # Determine the maximum line length
        max_length = max(len(line) for line in raw_grid)

        # Pad each line to ensure consistent length
        self.grid = [list(line.ljust(max_length)) for line in raw_grid]

        weight_iter = iter(self.stone_weights)
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell in {'$', '*'}:
                    try:
                        weight = next(weight_iter)
                        self.stones[(i, j)] = weight
                    except StopIteration:
                        self.stones[(i, j)] = 100

    def get_start_position(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == '@':
                    return i, j
        return None

    def update_position(self, x, y, symbol):
        self.grid[x][y] = symbol
