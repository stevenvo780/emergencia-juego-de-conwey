
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from concurrent.futures import ThreadPoolExecutor

# Grid size
N = 200
grid = np.random.choice([0, 1], N*N, p=[0.9, 0.1]).reshape(N, N)


def update_region(start_row, end_row, start_col, end_col, newGrid):
    for i in range(start_row, end_row):
        for j in range(start_col, end_col):
            total = int((grid[i, (j-1) % N] + grid[i, (j+1) % N] +
                         grid[(i-1) % N, j] + grid[(i+1) % N, j] +
                         grid[(i-1) % N, (j-1) % N] + grid[(i-1) % N, (j+1) % N] +
                         grid[(i+1) % N, (j-1) % N] + grid[(i+1) % N, (j+1) % N]) / 1)

            if grid[i, j] == 1:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = 0
            else:
                if total == 3:
                    newGrid[i, j] = 1


def update_parallel(data):
    global grid
    newGrid = grid.copy()

    with ThreadPoolExecutor() as executor:
        executor.submit(update_region, 0, N//2, 0, N//2, newGrid)
        executor.submit(update_region, N//2, N, 0, N//2, newGrid)
        executor.submit(update_region, 0, N//2, N//2, N, newGrid)
        executor.submit(update_region, N//2, N, N//2, N, newGrid)

    mat.set_data(newGrid)
    grid = newGrid
    return [mat]


# Set up animation
fig, ax = plt.subplots(figsize=(10, 10))
mat = ax.matshow(grid)
ani = animation.FuncAnimation(fig, update_parallel, blit=True)

plt.show()
