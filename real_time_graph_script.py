import matplotlib.pyplot as plt
import numpy as np
import cupy as cp
from matplotlib.animation import FuncAnimation


class RealTimeGraph:
    def __init__(self, game_of_life):
        self.game_of_life = game_of_life
        self.emergent_properties = []
        self.reductionist_properties = []

    def calculate_emergent_properties(self):
        # Actualiza el estado del juego
        self.game_of_life.update()

        # Convierte la matriz del juego de la vida a una matriz NumPy
        grid = cp.asnumpy(self.game_of_life.grid)

        # Cuenta cuántas células hay de cada tipo (0 o 1)
        unique, counts = np.unique(grid, return_counts=True)

        # Suma todas las células para obtener el total
        total_cells = np.sum(counts)

        # Calcula la probabilidad de cada tipo de célula
        probabilities = counts / total_cells

        # Calcula la entropía usando la fórmula de la entropía de Shannon
        entropy = -np.sum(probabilities * np.log2(probabilities))

        return entropy

    def calculate_reductionist_properties(self):
        # Actualiza el estado del juego
        self.game_of_life.update()

        # Convierte la matriz del juego de la vida a una matriz NumPy
        grid = cp.asnumpy(self.game_of_life.grid)

        # Cuenta el número total de células vivas (1s)
        live_cells = np.sum(grid)

        return live_cells

    def run(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        ax1.set_title('Emergent Properties')
        ax1.set_xlabel('Iterations')
        ax1.set_ylabel('Entropy')
        ax1.grid(True)
        ax2.set_title('Reductionist Properties')
        ax2.set_xlabel('Iterations')
        ax2.set_ylabel('Live Cells')
        ax2.grid(True)

        line1, = ax1.plot([], [], 'r', label='Entropy (Emergent)')
        line2, = ax2.plot([], [], 'g', label='Live Cells (Reductionist)')

        ax1.legend()
        ax2.legend()

        def init():
            # Inicializa las líneas del gráfico como vacías
            line1.set_data([], [])
            line2.set_data([], [])
            return line1, line2

        def update(frame):
            emergent = self.calculate_emergent_properties()
            reductionist = self.calculate_reductionist_properties()

            self.emergent_properties.append(emergent)
            self.reductionist_properties.append(reductionist)

            line1.set_data(range(len(self.emergent_properties)),
                           self.emergent_properties)
            line2.set_data(range(len(self.reductionist_properties)),
                           self.reductionist_properties)

            ax1.relim()
            ax1.autoscale_view()
            ax2.relim()
            ax2.autoscale_view()

            return line1, line2

        ani = FuncAnimation(fig, update, frames=None,
                            init_func=init, blit=True)
        plt.show()
