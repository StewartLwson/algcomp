from util.sound import Sound
from util.io import IO
from util.musicgenerator import MusicGenerator

gen = MusicGenerator()

melody, comp = gen.generate_jazz(melody_method="RS", comp_method = "MC", population = 10000, rule = 150, change_rule = True, history_mode = False,
                                 generations = 100, folder="tes6", filename="GA Test", bars = 16, amount = 1, order = 1)
