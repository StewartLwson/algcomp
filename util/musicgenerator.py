from algorithms.markovchain import Markov_Chain
from algorithms.hiddenmarkovmodel import HMM
from algorithms.cellularautomata import Cellular_Automata
from algorithms.randomstring import Random_String
from algorithms.geneticalgorithm import Genetic_Algorithm
from util.io import IO

import numpy as np

class MusicGenerator():
    """
    """
    def __init__(self):
        self.io = IO()
        self.scales = self.io.load_scales()

    def parse_blues(self, blues, key):
        """
        """
        training_data = []
        for _, details in blues.items():
            for detail, values in details.items():
                song = []
                if detail == key:
                    for value in values:
                        song.append(value[0] + value[1])
                    training_data.append(song)
        return training_data

    def parse_standard(self, standards, standard_name):
        """
        """
        training_data = []
        for standard, details in standards.items():
            if standard == standard_name:
                for detail, values in details.items():
                    song = []
                    if detail == "Chords":
                        if "A Section" in values.keys():
                            for value in values["A Section"]:
                                song.append(value[0] + value[1])
                        if "B Section" in values.keys():
                            for value in values["B Section"]:
                                song.append(value[0] + value[1])
                        if "C Section" in values.keys():
                            for value in values["C Section"]:
                                song.append(value[0] + value[1])
                        if "Intro" in values.keys():
                            for value in values["Intro"]:
                                song.append(value[0] + value[1])
                        if "Head" in values.keys():
                            for value in values["Head"]:
                                song.append(value[0] + value[1])
                        training_data.append(song)
        return training_data

    def parse_standards(self, standards):
        """
        """
        training_data = []
        for _, details in standards.items():
            for detail, values in details.items():
                song = []
                if detail == "Chords":
                    if "A Section" in values.keys():
                        for value in values["A Section"]:
                            song.append(value[0] + value[1])
                    if "B Section" in values.keys():
                        for value in values["B Section"]:
                            song.append(value[0] + value[1])
                    if "C Section" in values.keys():
                        for value in values["C Section"]:
                            song.append(value[0] + value[1])
                    if "Intro" in values.keys():
                        for value in values["Intro"]:
                            song.append(value[0] + value[1])
                    if "Head" in values.keys():
                        for value in values["Head"]:
                            song.append(value[0] + value[1])
                    training_data.append(song)
        return training_data

    def convert_notes(self, melody):
        """
        """
        converted = []
        for note in melody:
            converted.append((note, 5, 1))
        return converted

    def convert_chords(self, comp, npb=4):
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
            chord_length = npb
            converted.append(
                (chord_name, chord_type, chord_octave, chord_length))
        return converted

    def get_matrix(self, genre, name):
        """
        """
        if genre == "jazz":
            training_data = self.parse_standard(
                self.io.load_training_data("standard"), name)
        elif genre == "blues":
            training_data = self.parse_blues(
                self.io.load_training_data("12bblues"), name)
        mc = Markov_Chain(training_data=training_data, order=4, retrain=True)
        mc.train()
        return mc.get_states(), mc.get_matrix()

    def generate_melody(self, scale, bars, npb, melody_method, rule, change_rule):
        if melody_method == "CA":
            ca = Cellular_Automata()
            melody = ca.generate_melody(
                scale=scale, bars=bars, npb=npb, rule=rule)
            if(change_rule):
                rule = np.random.randint(1, 255)
        elif melody_method == "RS":
            rs = Random_String()
            melody = rs.generate_melody(scale=scale, bars=bars, npb=npb)
        return melody

    def generate_comp(self, bars, comp_method, training_data, order, training_melody=[]):
        chords = self.io.load_chords()
        if comp_method == "MC":
            mc = Markov_Chain(training_data=training_data, order=order, retrain=True)
            mc.train()
            comp = mc.generate_comp(length=bars)
        elif comp_method == "HMM":
            hmm = HMM(training_chords=training_data, training_melody=training_melody,
                      order=order, retrain=True, chords=chords)
            comp = hmm.generate_comp(length=bars)
        return comp

    def generate_blues(self, folder, saving=True,
                       melody_method="CA", rule=150,
                       change_rule=False, retrain=True, npb=8,
                       key="C", population_size=10, generations=30, filename="",
                       amount=100, history_mode = True):
        """
        """
        if amount > population_size:
            amount = population_size
        training_data = self.parse_blues(
            self.io.load_training_data("12bblues"), key)
        scale = self.scales["minor blues"][key]
        history = self.generate_blues_melodies(scale=scale,
                                               population_size=population_size,
                                               generations=generations,
                                               rule=rule,
                                               change_rule=change_rule,
                                               melody_method=melody_method,
                                               history_mode=history_mode)
        for c, v in enumerate(history):
            melodies, fitnesses = v
            for i in range(amount):
                melody = melodies[i]
                fitness = fitnesses[i]
                comp = self.generate_blues_comp(training_data)
                print("Generating Comp for Melody " + str(i + 1))
                melody = self.convert_notes(melody)
                comp = self.convert_chords(comp, npb=npb)
                if saving == True:
                    info = "MC -" + \
                        " Order: " + str(4) + \
                        str(melody_method) + \
                        " Genetic Algorithm -" \
                        " Population Size: " + str(population_size) + \
                        " Generations: " + str(generations) + \
                        " Fitness: " + str(fitness)
                    self.io.save_song(
                        folder, melody, comp, info, filename="Gen " + str(c + 1) + filename + str(i + 1))
        return melody, comp

    def generate_blues_comp(self, training_data):
        comp = self.generate_comp(bars=12, comp_method="MC", training_data=training_data, order=4)
        return comp

    def generate_blues_melodies(self, scale, population_size, generations,
                              rule, change_rule, melody_method, history_mode):
        ga = Genetic_Algorithm(scale=scale,
                               bars=12,
                               style="blues",
                               population_size=population_size,
                               generations=generations,
                               npb=8,
                               rule=rule,
                               change_rule=change_rule,
                               melody_method=melody_method)
        history = ga.get_history()
        if not history_mode:
            history = [ga.get_population()]
        return history

    def generate_blues_melody(self, key, bars, npb, melody_method, rule, change_rule):
        scale = self.scales["minor blues"][key]
        melody = self.generate_melody(scale=scale,
                                      bars=bars,
                                      npb=npb,
                                      melody_method=melody_method,
                                      rule=rule,
                                      change_rule=change_rule)
        return melody

    def generate_jazz(self, folder="jazz", saving=True,
                      melody_method="CA", rule=150, change_rule=False, bars=32, npb=8, key="C", population_size=10,
                      generations=30, filename="Jazz", amount=100, history_mode=False):
        """
        """
        if amount > population_size:
            amount = population_size
        scale = self.scales["major"][key]
        history = self.generate_jazz_melodies(population_size=population_size,
                                              generations=generations,
                                              other_scale=scale,
                                              key=key,
                                              melody_method=melody_method,
                                              history_mode=history_mode,
                                              rule=rule,
                                              change_rule=change_rule,
                                              plot=True)

        for c, v in enumerate(history):
            melodies, fitnesses = v
            for i in range(amount):
                melody = melodies[i]
                fitness = fitnesses[i]
                comp = self.generate_jazz_comp(training_melody=melody)
                print("Generation Comp for Melody " + str(i + 1))
                melody = self.convert_notes(melody)
                comp = self.convert_chords(comp, npb=npb)
                if saving == True:
                    info = "HMM" + \
                        " Order: " + str(1) + \
                        " Genetic Algorithm -" \
                        " Population Size: " + str(population_size) + \
                        " Generations: " + str(generations) + \
                        " Fitness: " + str(fitness)
                    self.io.save_song(
                        folder, melody, comp, info, filename="Gen " + str(c + 1) + filename + str(i + 1))
        return melody, comp

    def generate_jazz_comp(self, bars=16, training_melody=[], comp_method="HMM"):
        training_data = self.parse_standards(
            self.io.load_training_data("standards"))
        comp = self.generate_comp(bars=16, comp_method=comp_method,
                                  training_data=training_data, training_melody=training_melody,
                                  order=1)
        return comp

    def get_best_jazz_melody(self, key, population_size, generations, melody_method,
                             rule=1, change_rule=False):
        scale = self.scales["chromatic"][key]
        melodies = self.generate_jazz_melodies(scale=scale,
                                               population_size=population_size,
                                               generations=generations,
                                               rule=rule,
                                               change_rule=change_rule,
                                               melody_method=melody_method,
                                               history_mode=False)
        return melodies[0][0][0]

    def generate_jazz_melodies(self, other_scale, population_size, generations,
                               melody_method, key, history_mode, rule=1, change_rule=False, plot=True):
        scale = self.scales["chromatic"][key]
        ga = Genetic_Algorithm(scale=scale,
                               bars=16,
                               other_scale=other_scale,
                               style="chromatic",
                               population_size=population_size,
                               generations=generations,
                               npb=8,
                               rule=rule,
                               change_rule=change_rule,
                               melody_method=melody_method)
        ga.evolve(plot=plot)
        history = ga.get_history()
        if not history_mode:
            history = [ga.get_population()]
        return history

    def generate_jazz_melody(self, key, bars, npb, melody_method, chromatic,
                             rule=1, change_rule=False):
        """
        """
        if chromatic:
            scale = self.scales["chromatic"][key]
        else:
            scale = self.scales["major"][key]
        melody = self.generate_melody(scale=scale,
                                      bars=bars,
                                      npb=npb,
                                      melody_method=melody_method,
                                      rule=rule,
                                      change_rule=change_rule)
        return melody