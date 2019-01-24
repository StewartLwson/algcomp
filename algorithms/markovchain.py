#!/usr/bin/env python

import numpy as np
import json
import hashlib

# An n-gram Markov Chain that models the changes between chord sequences from
# training data
class Markov_Chain:
    # training_data is the list of example sequences used to train the model
    # retrain is used for telling the model to either use existing training
    # or train from the provided training data
    # order is the size of the n-gram or length of chords sequence for the model
    # training is the name of the JSON file where previous training has been stored
    def __init__(self, training_data, retrain = True, order = 1, training = ""):
        self.order = order
        if(retrain):
            self.training_data = training_data

            # Existing states in the training data
            self.states = self.get_states()

            # Possible transitions from states
            self.transitions = self.get_transitions()

            # Transition probabilites
            self.matrix = self.get_matrix()

            # Output training to JSON file
            self.save_training()
        else:
            self.training = training

            # Input training to model
            self.load_training()

    # Generates a list of all existing states in the training data
    def get_states(self):
        states = []
        for sequence in self.training_data:
            # Chord sequences are split into chunks of order length
            chunks = [sequence[x:x+self.order] for x in range(0, len(sequence),
            self.order)]
            for chunk in chunks:
                chunk_string = "".join(chunk)
                if chunk_string not in states:
                    states.append(chunk_string)
        return sorted(states)

    # Generates possible transitions from states to act as columns/rows for
    # probability matrix
    def get_transitions(self):
        transitions = []
        for row in self.states:
            t_row = []
            for column in self.states:
                t_row.append(row + column)
            transitions.append(t_row)
        return sorted(transitions)

    # Generates the probability matrix
    def get_matrix(self):
        # Matrix of transition probabilties (initially all set to 0)
        matrix = np.zeros([len(self.states), len(self.states)])
        # List of all exisiting transitions in input composition
        changes = []

        # Iterates through training data and adds each transition to the list
        for sequence in self.training_data:
            chunks = [sequence[x:x+self.order * 2] for x in range(0,
            len(sequence), self.order)]
            for chunk in chunks:
                if len(chunk) == self.order * 2:
                    changes.append("".join(chunk))
                else:
                    for chord in sequence[0:self.order]:
                        chunk.append(chord)
                    chunks.append("".join(chunk))

        # Iterates through transition list and adds 1 to the matrix each time a
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

    # Saves training from model to a JSON file
    def save_training(self):
        # Filename is hashed so that when training with new or different data,
        # it can be saved with a different unique filename
        filename = str(hashlib.sha1(str(self.training_data).encode("utf-8")).hexdigest())
        path = "./training/" + filename + ".json"

        # Dictionary to be converted to JSON that contains training
        data = {
            "states": self.states,
            "transitions": self.transitions,
            # Matrix converted from ndarray to normal list
            "matrix": self.matrix.tolist()
        }

        with open(path, "w") as outfile:
            json.dump(data, outfile)

    # Loads training from JSON file to model
    def load_training(self):
        path = "./training/" + self.training + ".json"

        data = {}

        with open(path, "r") as infile:
            data = json.load(infile)

        self.states = data["states"]
        self.transitions = data["transitions"]
        self.matrix = data["matrix"]

    # Generates compositions based on training
    # length is the length of the composition based in terms of sequences
    # start is the starting sequence for the composition
    def generate_comp(self, length, start):
        # Check if start is the same length as a sequence
        if len(start) != self.order:
            print("Starting sequence is not of order " + str(self.order))
            return

        current = start
        comp = []
        for chord in current:
            comp.append(chord)

        row = 0

        # Appends to compositions as long as the length has not been bypassed
        for _ in range(length - 1):
            for state in self.states:
                if current == state:
                    row = self.states.index(state)

            # Chooses a transition based on the current sequence
            change = np.random.choice(self.transitions[row], replace=True, p=self.matrix[row])

            # Appends the last part of the sequence to the composition
            current = change[self.order:self.order * 2]
            for chord in current:
                comp.append(chord)

        print("Compositon of " + str(len(comp)) + " chords: " + str(comp))
        return comp
