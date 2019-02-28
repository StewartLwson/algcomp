from algorithms.markovchain import Markov_Chain
from algorithms.cellularautomata import Cellular_Automata
from algorithms.geneticalgorithm import Genetic_Algorithm
from util.io import IO
from scales import *

class MusicGenerator():

    def __init__(self):
        self.io = IO()

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
            self.io.save_song(melody, melody, comp)
        return melody, comp


    def jazz(self, saving):
        mc = Markov_Chain(training_data=
        self.io.load_training_data("wjazz"), order=1, retrain=True)
        mc.train()
        ga = Genetic_Algorithm(scale=MAJOR_SCALE,
                            style="jazz", population_size=100, npb=4, rule=30)
        melodies = ga.get_population()
        melody = melodies[0]
        comp = mc.generate_comp(length=12, start="1")
        if saving == True:
            self.io.save_song(melody, melody, comp)
        return melody, comp

