import numpy as np
import json
import hashlib

class Markov_Chain:
    def __init__(self, training_data, retrain = True, order = 1, training = ""):
        self.order = order
        if(retrain):
            self.training_data = training_data
            # Finds all the existing states in the training data
            self.states = self.get_states()

            # Finds all possible transitions from states
            self.transitions = self.get_transitions()

            # Finds all transition probabilites
            self.matrix = self.get_matrix()

            self.save_training()
        else:
            self.training = training
            self.load_training()

    def get_states(self):
        states = []
        for sequence in self.training_data:
            chunks = [sequence[x:x+self.order] for x in range(0, len(sequence), self.order)]
            for chunk in chunks:
                chunk_string = "".join(chunk)
                if chunk_string not in states:
                    states.append(chunk_string)
        return sorted(states)

    def get_transitions(self):
        transitions = []
        for row in self.states:
            t_row = []
            for column in self.states:
                t_row.append(row + column)
            transitions.append(t_row)
        return sorted(transitions)

    def get_matrix(self):
        # Matrix of transition probabilties (initially all set to 0)
        matrix = np.zeros([len(self.states), len(self.states)])
        # List of all exisiting transitions in input composition
        changes = []

        # Iterates through input composition and adds each transition to the list
        for sequence in self.training_data:
            chunks = [sequence[x:x+self.order * 2] for x in range(0, len(sequence), self.order)]
            for chunk in chunks:
                if len(chunk) == self.order * 2:
                    changes.append("".join(chunk))
                else:
                    for chord in sequence[0:self.order]:
                        chunk.append(chord)
                    chunks.append("".join(chunk))

        # Iterates through transition list and adds to the matrix each time a
        # corresponding transition exists
        for c in changes:
            for t in range(len(self.transitions)):
                for i in range(len(self.transitions[t])):
                    if c == self.transitions[t][i]:
                        matrix[t][i] += 1

        # Iterates through the matrix and normalizes each row to contain values
        # corresponding to probability of transition taking place
        for m in range(len(matrix)):
            num = sum(matrix[m])
            if int(num) is not 0:
                for i in range(len(matrix[m])):
                    matrix[m][i] = (matrix[m][i] / num)
        return matrix

    def save_training(self):
        filename = str(hashlib.sha1(str(self.training_data).encode("utf-8")).hexdigest())
        path = "./training/" + filename + ".json"

        data = {
            "states": self.states,
            "transitions": self.transitions,
            "matrix": self.matrix.tolist()
        }
        with open(path, "w") as outfile:
            json.dump(data, outfile)

    def load_training(self):
        path = "./training/" + self.training + ".json"
        data = {}
        with open(path, "r") as infile:
            data = json.load(infile)
        self.states = data["states"]
        self.transitions = data["transitions"]
        self.matrix = data["matrix"]

    def generate_comp(self, length, start):
        if len(start) != self.order:
            print("Starting sequence is not of order " + str(self.order))
            return
        current = start
        comp = []
        for chord in current:
            comp.append(chord)
        i = 0
        row = 0
        while i < length - 1:
            for state in self.states:
                if current == state:
                    row = self.states.index(state)
            change = np.random.choice(self.transitions[row], replace=True, p=self.matrix[row])
            current = change[self.order:self.order * 2]
            for chord in current:
                comp.append(chord)
            i += 1
        print("Compositon of " + str(len(comp)) + " chords: " + str(comp))
        return comp
