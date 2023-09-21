
import cupy as cp


class GameOfLife:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = cp.random.choice(
            [0, 1], (self.rows, self.cols), p=[0.9, 0.1])

    def update(self):
        total_neighbours = (self.grid[:-2, :-2] + self.grid[:-2, 1:-1] + self.grid[:-2, 2:] +
                            self.grid[1:-1, :-2] + self.grid[1:-1, 2:] +
                            self.grid[2:, :-2] + self.grid[2:, 1:-1] + self.grid[2:, 2:])
        birth = (total_neighbours == 3) & (self.grid[1:-1, 1:-1] == 0)
        survive = ((total_neighbours == 2) | (total_neighbours == 3)) & (
            self.grid[1:-1, 1:-1] == 1)
        self.grid[...] = 0
        self.grid[1:-1, 1:-1][birth | survive] = 1
