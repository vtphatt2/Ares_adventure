class Maze:
    def __init__(self, filepath):
        self.grid = []
        self.stone_weights = []
        self.load_maze(filepath)

    def load_maze(self, filepath):
        with open(filepath, 'r') as f:
            self.stone_weights = list(map(int, f.readline().strip().split()))
            self.grid = [list(line.rstrip('\n')) for line in f]


    def get_start_position(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell == '@':
                    return i, j
        return None

    def update_position(self, x, y, symbol):
        self.grid[x][y] = symbol