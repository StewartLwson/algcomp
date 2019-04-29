#!/usr/bin/env python

import numpy as np
import json
import hashlib


class Markov_Chain:
    """
    An n-gram Markov Chain that models the changes between chord sequences
    from training data to generate a chord sequence.

    Parameters
    ----------
        training_data: list
            Example sequences used to train the model retrain is used for
            telling the model to either use existing trainingor train from
            the provided training data.
        retrain: bool, optional
            Whether the model is to be trained using the given training
            data or given a JSON training file.
        order: int, optional
            The size of the n-gram.
        training: str, optional
            The filename of a JSON training file.

    """

    def __init__(self, training_data, retrain=True, order=1,
                 training=""):
        self.order = order
        self.retrain = retrain
        self.training_data = training_data
        self.training = training

        self.states = []
        self.transitions = []
        self.matrix = []

        self.starting_states = []
        self.starting_probabilities = []

    def train(self):
        """
        Trains the model under the current settings

        """
        if self.retrain:
            self.states = self.get_states()
            self.transitions = self.get_transitions()
            self.matrix = self.get_matrix()
            self.save_training()
        else:
            self.load_training()

    def get_states(self):
        """
        Returns a list of all existing states in the training data.

        Chord sequences are split into chunks of order length and appended to
        states if they are unique. The returned states are sorted to
        ascendingly to group similar chord sequences.

        """
        states = []
        for chords in self.training_data:
            chunks = [chords[x:x+self.order] for x in range(0,
                                                            len(chords), self.order)]
            for chunk in chunks:
                chunk_string = " ".join(chunk)
                if chunk_string not in states:
                    states.append(chunk_string)
        return sorted(states)

    def get_transitions(self):
        """
        Returns a 2D list of all possible state transitions to act as the
        columns and rows for of the transition table that will match
        a probability matrix.

        """
        transitions = []
        for row in self.states:
            t_row = []
            for column in self.states:
                t_row.append([row, column])
            transitions.append(t_row)
        return sorted(transitions)

    def get_matrix(self):
        """
        Returns a probability matrix.

        The training data is iterated through and each state is added to a
        list of changes. The amount of occurences of each state is then added
        to the corresponding column and row of a matrix. Each row is then
        normalized between 0 and 1 to give the probability of each change.

        """
        matrix = np.zeros([len(self.states), len(self.states)])
        starting_states = []
        transitions = []

        for chords in self.training_data:
            states = []
            is_starting_state = True
            chunks = [chords[x:x+self.order] for x in range(0,
                    len(chords), self.order)]
            for chunk in chunks:
                chunk_string = " ".join(chunk)
                if is_starting_state:
                    starting_states.append(chunk_string)
                    is_starting_state = False
                states.append(chunk_string)

            for i in range(0, len(states)):
                if i < (len(states)) - 1:
                    transitions.append([states[i], states[i + 1]])
                else:
                    transitions.append([states[i]])

        self.starting_probabilities = np.zeros([len(self.states)])

        for transition in transitions:
            for row, row_contents in enumerate(self.transitions):
                for col, _ in enumerate(row_contents):
                    if transition == self.transitions[row][col]:
                        matrix[row][col] += 1

        for i, state in enumerate(self.states):
            for j, possible_state in enumerate(starting_states):
                if state == possible_state:
                    self.starting_probabilities[j] += 1

        num = sum(self.starting_probabilities)
        for i, prob in enumerate(self.starting_probabilities):
            self.starting_probabilities[i] = prob / num

        for m in range(len(matrix)):
            num = sum(matrix[m])
            if int(num) is not 0:
                for i in range(len(matrix[m])):
                    matrix[m][i] = (matrix[m][i] / num)
            else:
                matrix[m] = self.starting_probabilities
        return matrix

    def save_training(self):
        """
        Outputs JSON object that represents states, transitions and matrix
        to file. The filename is a hash of the string value of the training making
        each filename unique to that training.

        """

        filename = str(hashlib.sha1(str(self.training_data).encode("utf-8"))
                       .hexdigest())
        path = "./training/" + filename + ".json"

        data = {
            "states": self.states,
            "transitions": self.transitions,
            "matrix": self.matrix.tolist()
        }

        with open(path, "w") as outfile:
            json.dump(data, outfile)

    def load_training(self):
        """
        Sets states, transitions and matrix from loaded file.

        """
        path = "./training/" + self.training + ".json"

        data = {}

        with open(path, "r") as infile:
            data = json.load(infile)

        self.states = data["states"]
        self.transitions = data["transitions"]
        self.matrix = data["matrix"]

    def generate_comp(self, length, start="", matrix=[]):
        """
        Generates compositions based on training by appending states to the
        overall composition for a desired length.

        Parameters
        ----------
            length: int
                The length of the composition based in terms of sequences.
            start: str
                The the starting state for the composition.

        """
        if matrix == []:
            matrix = self.matrix
        if start == "":
            current = np.random.choice(
                self.states, replace=True, p=self.starting_probabilities)
        else:
            current = start
        comp = []
        comp.append(current)
        row = 0

        length = int(length / self.order)

        for _ in range(length - 1):
            for state in self.states:
                if current == state:
                    row = self.states.index(state)
                    possible = []
                    for transition in self.transitions[row]:
                        possible.append(transition[1])
            change = np.random.choice(possible, replace=True,
                                      p=matrix[row])
            current = change
            comp.append(current)
        final_comp = []
        for sequence in comp:
            final_comp += sequence.split(' ')
        return final_comp
