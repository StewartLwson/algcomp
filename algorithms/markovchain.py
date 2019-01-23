import numpy as np

class Markov_Chain:
    def __init__(self, training_data, order = 1):
        self.order = order
        self.training_data = training_data

        # Finds all the existing states in the training data
        self.states = self.get_states()

        # Finds all possible transitions from states
        self.transitions = self.get_transitions()

        # Finds all transition probabilites
        self.matrix = self.get_matrix()

    def get_states(self):
        states = []
        for sequence in self.training_data:
            for state in sequence:
                if state not in states:
                    states.append(state)
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
        matrix = np.zeros([3, 3])
        # List of all exisiting transitions in input composition
        changes = []

        # Iterates through input composition and adds each transition to the list
        for i in range(len(self.training_data)):
            for j in range(len(self.training_data[i])):
                if j < len(self.training_data[i]) - 1:
                    changes.append(self.training_data[i][j] + self.training_data[i][j+1])
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

    def generate_comp(self, length, start):
        current = start
        comp = [current]
        i = 0
        row = 0
        while i != length:
            for chord in self.states:
                if current is chord:
                    row = self.states.index(chord)
            change = np.random.choice(self.transitions[row], replace=True, p=self.matrix[row])
            current = change[1]
            comp.append(change[1])
            i += 1
        print("Compositon of " + str(length) + " chords: " + str(comp))
        return comp
