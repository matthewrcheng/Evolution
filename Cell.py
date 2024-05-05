import random

# Constants
GRID_SIZE = 10
MUTATION_RATE = 0.1
NUM_ORGANISMS = 10

# Define cell types
class Cell:
    def __init__(self, cell_type):
        self.cell_type = cell_type

    def action(self, organism, environment):
        pass

class MainCell(Cell):
    def __init__(self):
        super().__init__("main")

    def action(self, organism, environment):
        # Main cell actions
        organism.eat(environment)
        organism.turn()
        organism.move(environment)

class EyeCell(Cell):
    def __init__(self):
        super().__init__("eye")

    def action(self, organism, environment):
        # Eye cell actions
        pass

class MouthCell(Cell):
    def __init__(self):
        super().__init__("mouth")

    def action(self, organism, environment):
        # Mouth cell actions
        pass

class SpeedCell(Cell):
    def __init__(self):
        super().__init__("speed")

    def action(self, organism, environment):
        # Speed cell actions
        pass

class DefenseCell(Cell):
    def __init__(self):
        super().__init__("defense")

    def action(self, organism, environment):
        # Defense cell actions
        pass




