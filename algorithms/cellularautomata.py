import numpy as np

class Cellular_Automata:
    def __init__(self, starting_state = 1, rule = 150, steps = 100, npb = 4, apply_rule = "all",):
        self.rule = rule
        self.npb = npb
        self.apply_rule = "all"

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
    def generate_notes(self, scale, bars = 1, npb = 4):
        sequence = []
        if self.apply_rule == "sequence":
            self.rule = np.random.randint(0, 255)
        for _ in range(bars):
            bar = []
            if self.apply_rule == "bar":
                self.rule = np.random.randint(0, 255)
            self.generate_starting_state()
            self.evolve()
            for generation in self.grid:
                index = int(sum(generation) % len(scale))
                bar.append(scale[index])
                if len(bar) >= npb:
                    break
            for note in bar:
                sequence.append(note)
        return sequence

    def generate_rhythm(self, bars = 1, npb = 4):
        sequence = []
        self.rule = np.random.randint(0, 255)
        self.generate_starting_state()
        self.evolve()
        rest = ["-", 0]
        for generation in self.grid:
            index = int(sum(generation) % 2)
            sequence.append(rest[index])
            if len(sequence) >= npb:
                break
        return sequence

    def generate_target_sequence(self, scale, bars = 1, npb = 4):
        target_notes = self.generate_notes(scale, bars = 1, npb = 2)
        melody = [target_notes[0]]
        move_from = scale.index(target_notes[0])
        move_to = scale.index(target_notes[1])
        if move_from < move_to:
            notes = scale[move_from:move_to]
        elif move_from > move_to:
            notes = scale[move_to + 1:move_from + 1]
        else:
            notes = scale
        for _ in range(npb * bars - 2):
            melody.append(np.random.choice(notes))
        melody.append(target_notes[1])
        return melody

    def apply_rhythm(self, melody, rhythm):
        for i, note in enumerate(rhythm):
            if note == "-":
                melody[i] = "-"
        return melody

    def generate_melody(self, scale, bars = 1, npb = 4):
        melody = []
        for _ in range(bars):
            section = self.generate_target_sequence(scale, bars = 1, npb = npb)
            rhythm = self.generate_rhythm(bars = 1, npb = npb)
            section = self.apply_rhythm(section, rhythm)
            melody += section
        return melody


    def generate_call_response(self, scale, bars = 2, npb = 4):
        call = self.generate_target_sequence(scale, bars, npb)
        call_rhythm = self.generate_rhythm(bars, npb)
        response = self.generate_target_sequence(scale, bars, npb)
        response_rhythm = self.generate_rhythm(bars, npb)
        call = self.apply_rhythm(call, call_rhythm)
        response = self.apply_rhythm(response, response_rhythm)
        melody = call + response
        return melody

    def generate_blues_melody(self, scale, npb = 4):
        melody1 = self.generate_call_response(scale, bars = 4, npb=npb)
        melody2 = self.generate_call_response(scale, bars = 4, npb=npb)
        melody = melody1 + melody1 + melody2
        return melody





