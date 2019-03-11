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

    def twelve_bar_blues(self, saving):
        training_data = self.io.load_training_data("12bblues")
        print(training_data)
        mc = Markov_Chain(training_data=training_data, order=4, retrain=True)
        mc.train()
        ga = Genetic_Algorithm(scale=MINOR_BLUES,
                            style="blues", population_size=5, npb=4, rule=30)
        melodies = ga.get_population()
        melody = melodies[0]
        print("Melody: " + str(melody))
        comp = mc.generate_comp(length=3, start="1111")
        if saving == True:
            self.io.save_song(melody, "blues", melody, comp)
        return melody, comp

    def generate_jazz(self, start = "", saving = False):
        training_data = self.parse_standards(self.io.load_training_data("standards"))
        #mc = Markov_Chain(training_data=training_data, order=1, retrain=True)
        #mc.train()
        chords = self.io.load_chords()
        ga = Genetic_Algorithm(scale=self.scale, bars = 32, style="jazz", population_size=10, npb=4, rule=30)
        melodies = ga.get_population()
        melody = melodies[0]
        hmm = HMM(training_chords=training_data, training_melody=melody, order = 1, retrain=True, chords=chords)
        comp = hmm.generate_comp(length=32, start=start)
        if saving == True:
            info = "Markov Chain -" + \
                   " Order: " + str(hmm.order) + \
                   " Genetic Algorithm -" \
                   " Population Size: " + str(ga.population_size) + \
                   " Generations: " + str(ga.generations)
            self.io.save_song(melody, "jazz", melody, comp, info)
        return melody, comp

    def generate_jazz_comp(self, start = ""):
        training_data = self.parse_standards(self.io.load_training_data("standards"))
        mc = Markov_Chain(training_data=training_data, order=1, retrain=True)
        mc.train()
        comp = mc.generate_comp(length=32, start=start)
        return comp

