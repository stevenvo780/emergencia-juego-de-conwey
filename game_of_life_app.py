import pygame
import cupy as cp

pygame.init()

class App:
    def __init__(self, game_of_life):
        self.game_of_life = game_of_life
        self.cellSize = 10
        self.screenSize = [1600, 820]
        self.screen = pygame.display.set_mode(self.screenSize, pygame.RESIZABLE)
        pygame.display.set_caption("Conway's Game of Life GPU Optimized")
        self.keys_pressed = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
        self.view_offset = [0, 0]
        self.dragging = False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.keys_pressed:
                        self.keys_pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    if event.key in self.keys_pressed:
                        self.keys_pressed[event.key] = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.dragging = True
                    elif event.button == 4:
                        self.cellSize += 1
                    elif event.button == 5:
                        self.cellSize -= 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging = False
                elif event.type == pygame.MOUSEMOTION and self.dragging:
                    dx, dy = event.rel
                    self.view_offset[0] += dx
                    self.view_offset[1] += dy

            self.game_of_life.update()
            grid_np = cp.asnumpy(self.game_of_life.grid)
            self.screen.fill((0, 0, 0))
            for i in range(self.game_of_life.rows):
                for j in range(self.game_of_life.cols):
                    if grid_np[i, j] == 1:
                        pygame.draw.rect(self.screen, (255, 255, 255),
                                         (j*self.cellSize + self.view_offset[0], i*self.cellSize + self.view_offset[1], self.cellSize, self.cellSize))
            pygame.display.update()
            pygame.time.delay(100)
