from algorithms.markovchain import Markov_Chain
from algorithms.hiddenmarkovmodel import HMM
from algorithms.cellularautomata import Cellular_Automata
from algorithms.geneticalgorithm import Genetic_Algorithm
from util.io import IO

class MusicGenerator():

    def __init__(self):
        self.io = IO()
        self.scales = self.io.load_scales()
        self.scale = self.scales["major"]["C"]

    def parse_standards(self, standards):
        training_data = []
        for standard, details in standards.items():
            for detail, values in details.items():
                song = []
                if detail == "Chords":
                    for value in values["A Section"]:
                        song.append(value[0] + value[1])
                    for value in values["B Section"]:
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

    def generate_jazz(self, start = "", saving = False, comp_method = "HMM",
                      order=1, retrain=True, npb=4, population_size=10):
        training_data = self.parse_standards(
                        self.io.load_training_data("standards"))
        chords = self.io.load_chords()
        ga = Genetic_Algorithm(scale=self.scale, bars = 32, style="jazz",
        population_size=population_size, npb=npb, rule=30)
        melodies = ga.get_population()
        melody = melodies[0]
        if comp_method == "HMM":
            hmm = HMM(training_chords=training_data, training_melody=melody,
            order=order, retrain=retrain, chords=chords)
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
                   " Generations: " + str(ga.generations)
            self.io.save_song(melody, "jazz", melody, comp, info)
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

