from algorithms.markovchain import Markov_Chain
from algorithms.hiddenmarkovmodel import HMM
from algorithms.cellularautomata import Cellular_Automata
from algorithms.geneticalgorithm import Genetic_Algorithm
from util.io import IO

class MusicGenerator():

    def __init__(self):
        self.io = IO()
        self.scales = self.io.load_scales()

    def parse_blues(self, blues, key):
        training_data = []
        for _, details in blues.items():
            for detail, values in details.items():
                song = []
                if detail == key:
                    for value in values:
                        song.append(value[0] + value[1])
                    training_data.append(song)
        return training_data

    def parse_standards(self, standards):
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

    def convert_chords(self, comp, npb = 4):
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
            converted.append((chord_name, chord_type, chord_octave, chord_length))
        return converted

    def generate_blues(self, saving=True, order=1, retrain=True,
                       npb=8, key="C", population=10, generations=5):
        """
        """
        training_data = self.parse_blues(
                        self.io.load_training_data("12bblues"), key)
        mc = Markov_Chain(training_data=training_data,
                          order=order,
                          retrain=retrain)
        mc.train()
        scale = self.scales["minor blues"][key]
        ga = Genetic_Algorithm(scale=scale,
                                 bars=12,
                                 style="blues",
                                 population_size=population,
                                 generations=generations,
                                 npb=npb,
                                 rule=30)
        melodies, fitnesses = ga.get_population()
        melody = melodies[0]
        fitness = fitnesses[0]
        print("Fitness of melody: " + str(fitnesses[0]))
        melody = self.convert_notes(melody)
        comp = mc.generate_comp(length=12)
        comp = self.convert_chords(comp,
                                   npb = npb)
        if saving == True:
            info = "MC" + \
                   " Order: " + str(order) + \
                   " Genetic Algorithm -" \
                   " Population Size: " + str(ga.population_size) + \
                   " Generations: " + str(ga.generations) + \
                   " Fitness: " + str(fitness)
            self.io.save_song("blues", melody, comp, info,)
        return melody, comp


    def generate_jazz(self, folder, start="", saving=True, comp_method="HMM",
                      melody_method="CA", order=1, retrain=True, npb=8, key="C", population=10,
                      generations=5, filename = "", amount = 100):
        """
        """
        if amount > population:
            amount = population
        training_data = self.parse_standards(
                        self.io.load_training_data("standards"))
        chords = self.io.load_chords()
        scale = self.scales["major"][key]
        ga = Genetic_Algorithm(scale=scale,
                               bars = 32,
                               style="jazz",
                               population_size=population,
                               generations=generations,
                               npb=npb,
                               rule=30,
                               melody_method=melody_method)
        melodies, fitnesses = ga.get_population()
        for i in range(amount):
            melody = melodies[i]
            fitness = fitnesses[i]
            if comp_method == "HMM":
                hmm = HMM(training_chords=training_data, training_melody=melody,
                order=order, retrain=retrain, chords=chords)
                print("Generation Comp for Melody " + str(i + 1))
                comp = hmm.generate_comp(length=32, start=start)
            else:
                mc = Markov_Chain(training_data=training_data, order=order, retrain=retrain)
                mc.train()
                comp = mc.generate_comp(length=32, start=start)
            melody = self.convert_notes(melody)
            comp = self.convert_chords(comp, npb = npb)
            if saving == True:
                info = comp_method + \
                    " Order: " + str(order) + \
                    " Genetic Algorithm -" \
                    " Population Size: " + str(ga.population_size) + \
                    " Generations: " + str(ga.generations) + \
                    " Fitness: " + str(fitness)
                self.io.save_song(folder, melody, comp, info, filename= filename + str(i + 1))
        return melody, comp

    def generate_jazz_comp(self, start = "", saving = False, comp_method = "HMM",
                      order=1, retrain=True, npb=4, melody = []):
        training_data = self.parse_standards(
                        self.io.load_training_data("standards"))
        chords = self.io.load_chords()
        if comp_method == "HMM":
            hmm = HMM(training_chords=training_data, training_melody=melody,
            order=order, retrain=retrain, chords=chords)
            comp = hmm.generate_comp(length=32, start=start)
            melody = self.convert_notes(melody)
        else:
            mc = Markov_Chain(training_data=training_data, order=order, retrain=retrain)
            mc.train()
            comp = mc.generate_comp(length=32, start=start)
        comp = self.convert_chords(comp, npb = npb)
        if saving == True:
            info = comp_method + \
                   " Order: " + str(order) + \
            self.io.save_song(melody, "jazz", melody, comp, info)
        return comp

