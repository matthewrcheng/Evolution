import random
from Cell import *
from utils import *

directions = [(1,0), (0,1), (-1,0), (0,-1)]
# Define organism
class Organism:
    def __init__(self, MUTATION_RATE, x, y, id, health=100, hunger=100, speed=1, turn_ratio=0.8, nourishment=10, heal_limit=90,
                 diet=Diet.HERBIVORE, repro=Reproduction.ASEXUAL):
        self.mutation_rate = MUTATION_RATE
        self.x = x
        self.y = y
        self.direction = (1,0)
        self.id = id
        self.cells = [MainCell()]
        self.max_health = health
        self.max_hunger = hunger
        self.health = health
        self.hunger = hunger
        self.speed = speed
        self.turn_ratio = turn_ratio
        self.nourishment = nourishment
        self.heal_limit = heal_limit
        self.diet = diet
        self.reproduction = repro

    def turn(self):
        if random.random() > self.turn_ratio:
            self.direction = random.choice(directions)

    def eat(self, env):
        x = self.x+self.direction[0]
        y = self.y+self.direction[1]
        
        if x >= 0 and y >= 0 and x < env.grid_size and y < env.grid_size and env.grid[x][y] == 1:
            env.grid[x][y] = None
            self.hunger += self.nourishment
            self.hunger = min(self.hunger, self.max_hunger)
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

    def reproduce(self, env):
        if self.reproduction == Reproduction.ASEXUAL:
            pass
        else:
            pass

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
            if self.hunger > self.heal_limit:
                self.health += 1
                self.health = min(self.health, self.max_health)
        else:
            self.health -= 1
            print(f"{self.id}'s hunger is 0, taking damage {self.health}")