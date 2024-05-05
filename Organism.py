import random
from Cell import *

directions = [(1,0), (0,1), (-1,0), (0,-1)]
# Define organism
class Organism:
    def __init__(self, MUTATION_RATE, x, y, id):
        self.mutation_rate = MUTATION_RATE
        self.x = x
        self.y = y
        self.direction = (1,0)
        self.id = id
        self.cells = [MainCell()]
        self.health = 100
        self.hunger = 100
        self.speed = 1

    def turn(self):
        if random.random() > 0.8:
            self.direction = random.choice(directions)

    def eat(self, env):
        x = self.x+self.direction[0]
        y = self.y+self.direction[1]
        if x >= 0 and y >= 0 and x < env.grid_size and y < env.grid_size and env.grid[x][y] == 1:
            env.grid[x][y] = None
            self.hunger += 10
            self.hunger = min(self.hunger, 100)
            print(f"{self.id} ate. New hunger: {self.hunger}")

    def move(self, env):
        x = self.x + self.direction[0]
        y = self.y + self.direction[1]
        if x >= 0 and y >= 0 and x < env.grid_size and y < env.grid_size and not env.grid[x][y]:
            env.grid[self.x][self.y] = None
            env.grid[x][y] = self
            self.x = x
            self.y = y
            # print(f"{self.id} moved to {self.x},{self.y}")

    def mutate(self):
        if random.random() < self.mutation_rate:
            # Add new cell or modify existing one
            pass

    def action(self, environment):
        for cell in self.cells:
            cell.action(self, environment)
        if self.hunger > 0:
            self.hunger -= 1
            # print(f"{self.id}'s hunger is now {self.health}")
            if self.hunger > 90:
                self.health += 1
                self.health = min(self.health, 100)
        else:
            self.health -= 1
            print(f"{self.id}'s hunger is 0, taking damage {self.health}")