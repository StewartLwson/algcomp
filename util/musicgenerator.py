from algorithms.markovchain import Markov_Chain
from algorithms.hiddenmarkovmodel import HMM
from algorithms.cellularautomata import Cellular_Automata
from algorithms.geneticalgorithm import Genetic_Algorithm
from util.io import IO


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

    def generate_blues(self, folder, start="", saving=True,
                       melody_method="CA", order=1, rule=150,
                       change_rule=False, retrain=True, npb=8,
                       key="C", population=10, generations=30, filename="",
                       amount=100, history_mode = True):
        """
        """
        if amount > population:
            amount = population
        training_data = self.parse_blues(
            self.io.load_training_data("12bblues"), key)
        scale = self.scales["minor blues"][key]
        ga = Genetic_Algorithm(scale=scale,
                               bars=12,
                               style="blues",
                               population_size=population,
                               generations=generations,
                               npb=npb,
                               rule=rule,
                               change_rule=change_rule,
                               melody_method=melody_method)
        history = ga.get_history()
        if not history_mode:
            history = [ga.get_population()]
        for c, v in enumerate(history):
            melodies, fitnesses = v
            for i in range(amount):
                melody = melodies[i]
                fitness = fitnesses[i]
                mc = Markov_Chain(training_data=training_data,
                                    order=order, retrain=retrain)
                mc.train()
                print("Generating Comp for Melody " + str(i + 1))
                comp = mc.generate_comp(length=12, start=start)
                melody = self.convert_notes(melody)
                comp = self.convert_chords(comp, npb=npb)
                if saving == True:
                    info = "MC -" + \
                        " Order: " + str(order) + \
                        str(melody_method) + \
                        " Genetic Algorithm -" \
                        " Population Size: " + str(ga.population_size) + \
                        " Generations: " + str(ga.generations) + \
                        " Fitness: " + str(fitness)
                    self.io.save_song(
                        folder, melody, comp, info, filename="Gen " + str(c + 1) + filename + str(i + 1))
        return melody, comp

    def generate_jazz(self, folder, start="", saving=True, comp_method="HMM",
                      melody_method="CA", order=1, rule=150, change_rule=False, retrain=True, bars=32, npb=8, key="C", population=10,
                      generations=30, filename="", amount=100, history_mode = False):
        """
        """
        if amount > population:
            amount = population
        training_data = self.parse_standards(
            self.io.load_training_data("standards"))
        chords = self.io.load_chords()
        scale = self.scales["chromatic"][key]
        other_scale = self.scales["major"][key]
        ga = Genetic_Algorithm(scale=scale,
                               bars=bars,
                               style="chromatic",
                               population_size=population,
                               generations=generations,
                               other_scale=other_scale,
                               npb=npb,
                               rule=rule,
                               change_rule=change_rule,
                               melody_method=melody_method)
        history = ga.get_history()
        if not history_mode:
            history = [ga.get_population()]
        for c, v in enumerate(history):
            melodies, fitnesses = v
            for i in range(amount):
                melody = melodies[i]
                fitness = fitnesses[i]
                if comp_method == "HMM":
                    hmm = HMM(training_chords=training_data, training_melody=melody,
                              order=order, retrain=retrain, chords=chords)
                    print("Generation Comp for Melody " + str(i + 1))
                    comp = hmm.generate_comp(length=bars, start=start)
                else:
                    mc = Markov_Chain(training_data=training_data,
                                      order=order, retrain=retrain)
                    mc.train()
                    comp = mc.generate_comp(length=bars, start=start)
                melody = self.convert_notes(melody)
                comp = self.convert_chords(comp, npb=npb)
                if saving == True:
                    info = comp_method + \
                        " Order: " + str(order) + \
                        " Genetic Algorithm -" \
                        " Population Size: " + str(ga.population_size) + \
                        " Generations: " + str(ga.generations) + \
                        " Fitness: " + str(fitness)
                    self.io.save_song(
                        folder, melody, comp, info, filename="Gen " + str(c + 1) + filename + str(i + 1))
        return melody, comp
