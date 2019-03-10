from algorithms.markovchain import Markov_Chain
from algorithms.cellularautomata import Cellular_Automata
from algorithms.geneticalgorithm import Genetic_Algorithm
from util.io import IO

class MusicGenerator():

    def __init__(self):
        self.io = IO()

    def convert_notes(self, melody):
        converted = []
        for note in melody:
            converted.append((note, 4, 1))
        return converted

    def convert_chords(self, comp):
        converted = []
        for chord in comp:
            if not chord[1] == "#" or chord[1] == "b":
                chord_name = chord[0]
                chord_type = chord[1:]
            else:
                chord_name = chord[0:1]
                chord_type = chord[2:]
            chord_octave = 4
            chord_length = 4
            converted.append((chord_name, chord_type, chord_octave, chord_length))
        return converted

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

    def jazz(self, saving):
        mc = Markov_Chain(training_data=
        self.io.load_training_data("wjazz"), order=1, retrain=True)
        mc.train()
        ga = Genetic_Algorithm(scale=MAJOR_SCALE,
                            style="jazz", population_size=10, npb=4, rule=30)
        melodies = ga.get_population()
        melody = melodies[0]
        comp = mc.generate_comp(length=24, start="1")
        if saving == True:
            self.io.save_song(melody, "jazz", melody, comp)
        return melody, comp

