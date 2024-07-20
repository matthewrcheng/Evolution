import random
import logging
from utils import *

directions = [(1,0), (0,1), (-1,0), (0,-1)]

class Environment:
    def __init__(self, GRID_SIZE: int, logger):
        self.curr_id = 0
        self.grid_size = GRID_SIZE
        self.logger = logger
        self.org_logger = logging.getLogger('organism')
        self.org_logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler('organism.log')
        self.org_logger.addHandler(file_handler)
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.organisms = dict()
        self.new_organisms = []

    def init_organisms(self, num_organisms: int, mutation_rate: float):
        for _ in range(num_organisms):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            organism = Organism(mutation_rate, x, y, self.curr_id, self, Sex.ASEXUAL)
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
            self.logger.info(f"{organism.id} has died")
        self.spawn_food()

class Organism:
    def __init__(self, mutation_rate: float, x:int, y:int, id:int, env:Environment, sex:Sex, health:int=100, hunger:int=100, speed:int=1,
                strength:int=0.1,turn_ratio:float=0.8, nourishment:int=10, heal_limit:int=90, diet=Diet.HERBIVORE, repro=Reproduction.ASEXUAL,
                repro_rate:float=0.001, offspring_term_limit:int=10, fertility:float=0.5, color=RED):
        self.mutation_rate = mutation_rate
        self.x = x
        self.y = y
        self.direction = (1,0)
        self.id = id
        self.env = env
        self.sex = sex
        self.max_health = health
        self.max_hunger = hunger
        self.health = health
        self.hunger = hunger
        self.speed = speed
        self.strength = strength
        self.turn_ratio = turn_ratio
        self.nourishment = nourishment
        self.heal_limit = heal_limit
        self.diet = diet
        self.reproduction = repro
        self.reproduction_rate = repro_rate
        self.gravid = False
        self.offspring_term = 0
        self.offspring_term_limit = offspring_term_limit
        self.fertility = fertility
        self.color = color
        self.env.org_logger.info(f"{self.id}: {str(self)}")
        self.turn()

    def __str__(self):
        return f"Organism {self.id} - Mutation Rate: {self.mutation_rate} Sex {self.sex} Health: {self.max_health} Hunger: {self.max_hunger} Speed: {self.speed} Strength: {self.strength} Turn Ratio: {self.turn_ratio} Nourishment: {self.nourishment} Heal Limit: {self.heal_limit} Diet: {self.diet} Reproduction: {self.reproduction} Reproduction Rate: {self.reproduction_rate} Fertility: {self.fertility} Offspring Term Limit: {self.offspring_term_limit} Color: {self.color}"

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

        if self.diet == Diet.HERBIVORE or self.diet == Diet.OMNIVORE:
            if self.check_dims(x, y) and self.env.grid[x][y] == 1:
                self.env.grid[x][y] = None
                self.hunger += self.nourishment
                self.hunger = min(self.hunger, self.max_hunger)
                # print(f"{self.id} ate. New hunger: {self.hunger}")
        if self.diet == Diet.CARNIVORE or self.diet == Diet.OMNIVORE: 
            if self.check_dims(x, y):
                target = self.env.grid[x][y] 
                if type(target) == Organism:
                    success = self.attack(target)
                    if success:
                        self.env.grid[x][y] = None
                        self.hunger += self.nourishment
                        self.hunger = min(self.hunger, self.max_hunger)
                        self.env.logger.info(f"{self.id} ate target {target.id}")

    def attack(self, other):
        self.env.logger.info(f"{self.id} is attacking {other.id}")
        if self.speed >= other.speed:
            while self.health > 0 and other.health > 0:
                if random.random() < self.strength:
                    other.health -= self.strength*65
                if random.random() < other.strength:
                    self.health -= other.strength*35
        else:
            if random.random() * self.strength > random.random() * other.strength:
                while other.health > 0 and self.health > 0:
                    if random.random() < other.strength:
                        self.health -= other.strength*55
                    if random.random() < self.strength:
                        other.health -= self.strength*45
            else:
                self.env.logger.info(f"{other.id} got away!")
                return False
        if other.health <= 0:
            other.health = 0
            return True
        else:
            self.env.logger.info(f"{self.id} failed the attack and died.")
            self.health = 0
            return False

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
                child = Organism(self.mutation_rate, x, y, 0, self.env, Sex.ASEXUAL, self.max_health, self.max_hunger, self.speed, self.strength, self.turn_ratio, self.nourishment,
                                 self.heal_limit, self.diet, self.reproduction, self.reproduction_rate, 0, 0, self.color)
            
                child.turn(self.turn_around())
                child.mutate()
                self.env.queue_organism(child)
                self.env.logger.info(f"{self.id} produced a child")
        else:
            x = self.x - self.direction[0]
            y = self.y - self.direction[1]
            if self.check_dims(x, y) and not self.env.grid[x][y]:
                child = Organism(self.gaussian_stat("mutation_rate"), x, y, 0, self.env, random.choice([Sex.MALE, Sex.FEMALE]), self.gaussian_stat("max_health"),
                                 self.gaussian_stat("max_hunger"), self.gaussian_stat("speed"), self.gaussian_stat("strength"), self.gaussian_stat("turn_ratio"),
                                 self.gaussian_stat("nourishment"), self.gaussian_stat("heal_limit"), self.offspring_categorical_stat("diet"), self.reproduction,
                                 self.gaussian_stat("reproduction_rate"), self.gaussian_stat("offspring_term_limit"), self.gaussian_stat("fertility"), self.offspring_color())
            
                child.turn(self.turn_around())
                child.mutate()
                self.env.queue_organism(child)
                self.env.logger.info(f"{self.id} produced a child with {self.baby_daddy.id}")

    def gaussian_stat(self, stat):
        return random.gauss((getattr(self,stat)+getattr(self.baby_daddy,stat))/2, getattr(self, stat)/100)
    
    def offspring_categorical_stat(self, stat):
        return random.choice([getattr(self,stat), getattr(self.baby_daddy,stat)])
    
    def offspring_color(self):
        dr = random.random()
        dg = random.random()
        db = random.random()
        return (clamp(int(self.color[0]*dr+self.baby_daddy.color[0]*(1-dr)+random.uniform(-5,5))), clamp(int(self.color[1]*dg+self.baby_daddy.color[1]*(1-dg)+random.uniform(-5,5))), clamp(int(self.color[2]*db+self.baby_daddy.color[2]*(1-db)+random.uniform(-5,5))))

    def check_male_mate(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.check_dims(self.x+i, self.y+j):
                    if type(self.env.grid[self.x+i][self.y+j]) == Organism and self.env.grid[self.x+i][self.y+j].sex == Sex.MALE and self.env.grid[self.x+i][self.y+j].reproduction == self.reproduction:
                        return self.env.grid[self.x+i][self.y+j]

    def conceive_check(self, male):
        total_fertility = male.fertility + self.fertility
        if random.random() < total_fertility:
            self.conceive(male)

    def conceive(self, male):
        self.gravid = True
        self.baby_daddy = male
    
    def mutate(self):
        if random.random() < self.mutation_rate:
            # Add new cell or modify existing one
            stat = random.choice(["mutation_rate", "max_health", "max_hunger", "speed", "turn_ratio", "nourishment", "heal_limit", "diet", "reproduction", "reproduction_rate", "fertility", "offspring_term_limit", "color"])
            random_stat = "random_" + stat
            value = globals()[random_stat]()
            setattr(self, stat, value)
            self.env.logger.info(f"{self.id} mutated {stat} to {value}")
    
    def action(self):
        self.eat()
        self.turn()
        self.move()
        if self.reproduction == Reproduction.ASEXUAL:
            if random.random() < self.reproduction_rate:
                self.reproduce()
        else:
            if self.gravid:
                self.offspring_term += 1
                if self.offspring_term > self.offspring_term_limit:
                    self.gravid=False
                    self.offspring_term = 0
                    self.reproduce()
            if self.sex == Sex.FEMALE:
                male = self.check_male_mate()
                if male:
                    self.conceive_check(male)
        if self.hunger > 0:
            self.hunger -= 1
            # print(f"{self.id}'s hunger is now {self.health}")
            if self.hunger > self.heal_limit:
                self.health += 1
                self.health = min(self.health, self.max_health)
        else:
            self.health -= 1
            # print(f"{self.id}'s hunger is 0, taking damage {self.health}")