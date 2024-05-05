
import random
from Organism import *

class Environment:
    def __init__(self, GRID_SIZE):
        self.curr_id = 0
        self.grid_size = GRID_SIZE
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.organisms = dict()

    def init_organisms(self, num_organisms, mutation_rate):
        for _ in range(num_organisms):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            organism = Organism(mutation_rate, x, y, self.curr_id)
            self.add_organism(self.curr_id, organism, x, y)
            self.curr_id += 1

    def spawn_food(self):
        for _ in range(random.randint(0,2)):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            self.set_food(x,y)


    def set_food(self, x, y):
        if self.grid[x][y] == None:
            self.grid[x][y] = 1

    def add_organism(self, id, organism, x, y):
        self.organisms[id] = organism
        self.grid[x][y] = organism

    def remove_organism(self, organism):
        self.organisms.pop(organism.id)
        self.grid[organism.x][organism.y] = None

    def tick(self):
        to_remove = []
        for organism in self.organisms.values():
            organism.action(self)
            if organism.health == 0:
                to_remove.append(organism)
        for organism in to_remove:
            self.remove_organism(organism)
            print(f"{organism.id} has died")
        self.spawn_food()
        