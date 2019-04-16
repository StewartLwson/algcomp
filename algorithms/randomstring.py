import numpy as np

class Random_String:

    def __init__(self):
        pass

    def generate_notes(self, scale, bars = 1, npb = 4):
        sequence = []
        beats = range(bars * npb)
        for _ in beats:
            sequence.append(np.random.choice(scale))
        return sequence

    def generate_rhythm(self, bars = 1, npb = 4):
        rest = ["-", 0]
        sequence = []
        beats = range(bars * npb)
        for _ in beats:
            sequence.append(np.random.choice(rest))
        return sequence

    def apply_rhythm(self, melody, rhythm):
        for i, note in enumerate(rhythm):
            if note == "-":
                melody[i] = "-"
        return melody

    def generate_melody(self, scale, rhythms_amount = 4, bars = 1, npb = 4):
        melody = []
        rhythms = []
        for _ in range(rhythms_amount):
            rhythm = self.generate_rhythm(bars = 1, npb = npb)
            rhythms.append(rhythm)
        for _ in range(bars):
            section = self.generate_notes(scale, bars = 1, npb = npb)
            rhythm = rhythms[np.random.choice(range(rhythms_amount))]
            section = self.apply_rhythm(section, rhythm)
            melody += section
        return melody
