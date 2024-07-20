import random
from enum import Enum

def clamp(x: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(x, maximum))

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

class Diet(Enum):
    HERBIVORE = 0
    OMNIVORE = 1
    CARNIVORE = 2

class Reproduction(Enum):
    ASEXUAL = 0
    OVIPARITY = 1 
    VIVIPARITY = 2

class Sex(Enum):
    ASEXUAL = 0
    MALE = 1
    FEMALE = 2

def random_mutation_rate() -> float:
    return random.random()

def random_max_health() -> int:
    return random.randint(50, 300)

def random_max_hunger() -> int:
    return random.randint(50, 300)

def random_speed() -> int:
    return random.randint(1, 5)

def random_turn_ratio() -> float:
    return random.random()

def random_nourishment() -> int:
    return random.randint(1, 10)    

def random_heal_limit() -> int:
    return random.randint(50, 300)

def random_diet() -> Diet:
    return random.choice([Diet.HERBIVORE, Diet.OMNIVORE, Diet.CARNIVORE])

def random_reproduction() -> Reproduction:
    return random.choice([Reproduction.ASEXUAL, Reproduction.OVIPARITY, Reproduction.VIVIPARITY])

def random_reproduction_rate() -> float:
    return random.random()/25

def random_fertility() -> float:
    return random.random()

def random_offspring_term_limit() -> int:
    return random.randint(0, 100)

def random_color() -> tuple:
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))