import numpy as np

class Cellular_Automata:
    def __init__(self, starting_state = 1, rule = 150, steps = 100):
        # Rule number
        self.rule = rule

        # Binary representation of rule number
        self.output_pattern = [int(x) for x in np.binary_repr(self.rule, width=8)]

        # Binary representations of all numbers going down from 8
        self.input_pattern = np.zeros([8, 3])
        for i in range(8):
            self.input_pattern[i, :] = [int(x) for x in np.binary_repr(7-i, width=3)]

        # Size of Cellular Automata grid defined by steps of lifecrycle of the CA
        self.steps = steps
        self.columns = steps + 1
        self.rows = int(self.columns/2)+1
        self.grid = np.zeros([self.rows, self.columns+2])

        # Starting state of CA
        self.starting_state = np.zeros([self.columns+2])
        self.starting_state[int(self.columns/2)+1] = 1
        self.set_starting_state(self.starting_state)

    def set_starting_state(self, state):
        self.grid[0] = state

    def generate_starting_state(self):
        self.starting_state = np.zeros([self.columns+2])
        for i, _ in enumerate(self.starting_state):
            self.starting_state[i] = np.random.randint(0, 2)
        self.set_starting_state(self.starting_state)

    def evolve(self):
        # Applies rule to grid according to starting position
        for i in np.arange(0, self.rows-1):
            for j in np.arange(0, self.columns):
                for k in range(8):
                    if np.array_equal(self.input_pattern[k, :], self.grid[i, j:j+3]):
                        self.grid[i+1, j+1] = self.output_pattern[k]


    # Algorithm for generating compositions. The sum of the alive cells every
    # generation is recording and checked if it exists in the scale.
    def generate_melody(self, scale, bars = 12, npb = 4, rest_chance = 20, rule = 150):
        sequence = []
        random = False
        if rule == "random":
            random = True
        else:
            self.rule = rule
        for _ in range(bars):
            bar = []
            if random:
                self.rule = np.random.randint(0, 255)
            print(self.rule)
            self.generate_starting_state()
            self.evolve()
            for generation in self.grid:
                sum = 0
                for num in generation:
                    sum = sum + num
                sum = sum % 13
                if sum in scale:
                    bar.append(int(sum))
                else:
                    if np.random.randint(0, 100) < rest_chance:
                        bar.append("-")
                if len(bar) >= npb:
                    break
            for note in bar:
                sequence.append(note)
        print("Composition: " + str(sequence))
        return sequence