
import matplotlib.pyplot as plt
import numpy as np
from game_of_life import GameOfLife
import cupy as cp


def calculate_emergent_properties(game_of_life, iterations):
    entropy_list = []
    for _ in range(iterations):
        game_of_life.update()
        grid = cp.asnumpy(game_of_life.grid)
        unique, counts = np.unique(grid, return_counts=True)
        total_cells = np.sum(counts)
        probabilities = counts / total_cells
        entropy = -np.sum(probabilities * np.log2(probabilities))
        entropy_list.append(entropy)
    return entropy_list


def calculate_reductionist_properties(game_of_life, iterations):
    live_cells_list = []
    for _ in range(iterations):
        game_of_life.update()
        grid = cp.asnumpy(game_of_life.grid)
        live_cells = np.sum(grid)
        live_cells_list.append(live_cells)
    return live_cells_list


if __name__ == "__main__":
    game_of_life = GameOfLife(100, 100)
    iterations = 100

    emergent_properties = calculate_emergent_properties(
        game_of_life, iterations)
    reductionist_properties = calculate_reductionist_properties(
        game_of_life, iterations)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(range(iterations), emergent_properties,
             label='Entropy (Emergent)')
    plt.title('Emergent Properties')
    plt.xlabel('Iterations')
    plt.ylabel('Entropy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(range(iterations), reductionist_properties,
             label='Live Cells (Reductionist)')
    plt.title('Reductionist Properties')
    plt.xlabel('Iterations')
    plt.ylabel('Live Cells')
    plt.legend()

    plt.tight_layout()
    plt.show()
