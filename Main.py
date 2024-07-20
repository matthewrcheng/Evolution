import random
import pygame
from Evolution import *

# Constants
GRID_SIZE = 25
CELL_SIZE = 10
MUTATION_RATE = 0.1
NUM_ORGANISMS = 10

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
pygame.display.set_caption("Evolution Simulator")
clock = pygame.time.Clock()

def main():
    # Initialize environment
    env = Environment(GRID_SIZE)

    env.init_organisms(NUM_ORGANISMS, MUTATION_RATE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(WHITE)

        # Draw grid lines
        for x in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, GRID_SIZE * CELL_SIZE))
        for y in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (0, y), (GRID_SIZE * CELL_SIZE, y))

        # Draw organisms
        for organism in env.organisms.values():
            pygame.draw.rect(screen, organism.color, (organism.x * CELL_SIZE, organism.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for i in range(len(env.grid)):
            for j in range(len(env.grid[i])):
                if env.grid[i][j] == 1:
                    pygame.draw.rect(screen, GREEN, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Update display
        pygame.display.flip()

        # Tick the environment
        env.tick()

        # Cap the frame rate
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()