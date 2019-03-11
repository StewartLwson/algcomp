import numpy as np
from algorithms.markovchain import Markov_Chain

class HMM():
    """
    """
    def __init__(self, training_chords, training_melody, retrain = True, order = 1, training = "", chords = {}):
        self.mc = Markov_Chain(training_chords, retrain, order, training)
        self.mc.train()

        self.states = self.mc.get_states()
        self.transitions = self.mc.get_transitions()
        self.matrix = self.mc.get_matrix()

        self.chords = chords

        self.order = order
        self.training_melody = training_melody

    def convert_chords(self, comp):
        """
        """
        converted = []
        for chord in comp:
            if chord[1] == "#" or chord[1] == "b":
                chord_name = chord[0:2]
                chord_type = chord[2:]
            else:
                chord_name = chord[0]
                chord_type = chord[1:]

            chord_octave = 4
            chord_length = 4
            converted.append((chord_name, chord_type, chord_octave, chord_length))
        return converted

    def get_matrix(self):
        matrix = np.zeros([len(self.states), len(self.states)])
        melody_fragments = [self.training_melody[x:x+self.order * 4] for x in range(0, len(self.training_melody), self.order * 4)]
        arpeggios = []
        chords = self.convert_chords(self.states)
        for chord in chords:
            chord_notes = self.chords[chord[1]][chord[0]]
            arpeggios.append(chord_notes)
        for fragment in melody_fragments:
            for note in fragment:
                for i, arp in enumerate(arpeggios):
                    if note in arp and not note == "-":
                        for j in range(len(matrix)):
                            matrix[j][i] += 1
        for m in range(len(matrix)):
            num = sum(matrix[m])
            if int(num) is not 0:
                for i in range(len(matrix[m])):
                    matrix[m][i] = (matrix[m][i] / num)
        matrix = matrix + self.matrix
        for row in matrix:
            num = sum(row)
            for i, col in enumerate(row):
                row[i] = col / num
        print(matrix)
        return matrix

    def generate_comp(self, length, start = ""):
        matrix = self.get_matrix()
        comp = self.mc.generate_comp(length, start, matrix)
        return comp
