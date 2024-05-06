import random
from utils import *

directions = [(1,0), (0,1), (-1,0), (0,-1)]

class Environment:
    def __init__(self, GRID_SIZE: int):
        self.curr_id = 0
        self.grid_size = GRID_SIZE
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.organisms = dict()
        self.new_organisms = []

    def init_organisms(self, num_organisms: int, mutation_rate: float):
        for _ in range(num_organisms):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            organism = Organism(mutation_rate, x, y, self.curr_id, self)
            self.add_organism(organism, x, y)

    def spawn_food(self): 
        for _ in range(random.randint(0,2)):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            self.set_food(x,y)


    def set_food(self, x: int, y: int):
        if self.grid[x][y] == None:
            self.grid[x][y] = 1

    def queue_organism(self, organism):
        self.new_organisms.append(organism)

    def add_organism(self, organism, x: int, y: int):
        self.organisms[self.curr_id] = organism
        organism.id = self.curr_id
        self.grid[x][y] = organism
        self.curr_id += 1

    def remove_organism(self, organism):
        self.organisms.pop(organism.id)
        self.grid[organism.x][organism.y] = None

    def tick(self):
        to_remove = []
        while self.new_organisms:
            organism = self.new_organisms.pop()
            self.add_organism(organism, organism.x, organism.y)
        for organism in self.organisms.values():
            organism.action()
            if organism.health == 0:
                to_remove.append(organism)
        for organism in to_remove:
            self.remove_organism(organism)
            print(f"{organism.id} has died")
        self.spawn_food()

class Organism:
    def __init__(self, MUTATION_RATE: float, x:int, y:int, id:int, env:Environment, health:int=100, hunger:int=100, speed:int=1,
                turn_ratio:float=0.8, nourishment:int=10, heal_limit:int=90, diet=Diet.HERBIVORE, repro=Reproduction.ASEXUAL,
                repro_rate:float=0.001):
        self.mutation_rate = MUTATION_RATE
        self.x = x
        self.y = y
        self.direction = (1,0)
        self.id = id
        self.env = env
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
        self.reproduction_rate = repro_rate

    def check_dims(self, x: int, y: int):
        return x >= 0 and y >= 0 and x < self.env.grid_size and y < self.env.grid_size

    def turn(self, direction=None):
        if direction:
            self.direction = direction
        else:
            if random.random() > self.turn_ratio:
                self.direction = random.choice(directions)

    def turn_around(self):
        return (self.direction[0]*-1, self.direction[1]*-1)

    def eat(self):
        x = self.x+self.direction[0]
        y = self.y+self.direction[1]

        if self.check_dims(x, y) and self.env.grid[x][y] == 1:
            self.env.grid[x][y] = None
            self.hunger += self.nourishment
            self.hunger = min(self.hunger, self.max_hunger)
            # print(f"{self.id} ate. New hunger: {self.hunger}")

    def move(self):
        x = self.x + self.direction[0]
        y = self.y + self.direction[1]
        if self.check_dims(x, y) and not self.env.grid[x][y]:
            self.env.grid[self.x][self.y] = None
            self.env.grid[x][y] = self
            self.x = x
            self.y = y
            # print(f"{self.id} moved to {self.x},{self.y}")

    def reproduce(self):
        if self.reproduction == Reproduction.ASEXUAL:
            x = self.x - self.direction[0]
            y = self.y - self.direction[1]
            if self.check_dims(x, y) and not self.env.grid[x][y]:
                child = Organism(self.mutation_rate, x, y, 0, self.env, self.max_health, self.hunger, self.speed, self.turn_ratio, self.nourishment,
                                 self.heal_limit, self.diet, self.reproduction, self.reproduction_rate)
            
                child.turn(self.turn_around())
                child.mutate()
                self.env.queue_organism(child)
                print(f"{self.id} produced a child")
        else:
            pass

    def mutate(self):
        if random.random() < self.mutation_rate:
            # Add new cell or modify existing one
            pass

    def action(self):
        self.eat()
        self.turn()
        self.move()
        if random.random() < self.reproduction_rate:
            self.reproduce()
        if self.hunger > 0:
            self.hunger -= 1
            # print(f"{self.id}'s hunger is now {self.health}")
            if self.hunger > self.heal_limit:
                self.health += 1
                self.health = min(self.health, self.max_health)
        else:
            self.health -= 1
            # print(f"{self.id}'s hunger is 0, taking damage {self.health}")