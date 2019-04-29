from util.sound import Sound
from util.io import IO
from util.musicgenerator import MusicGenerator

io = IO()
snd = Sound()
gen = MusicGenerator()

# melody = gen.get_best_jazz_melody(key="F#", population_size=10000, generations=50, melody_method="RS")
# comp1 = gen.generate_jazz_comp(comp_method="MC")
# comp2 = gen.generate_jazz_comp(comp_method="HMM", melody=melody)
# melody = gen.convert_notes(melody)
# comp1 = gen.convert_chords(comp1, npb=8)
# comp2 = gen.convert_chords(comp2, npb=8)
# io.save_song("test", melody, comp1, info="", filename="MC Test")
# io.save_song("test", melody, comp2, info="", filename="HMM Test")
melody, comp1 = io.load_song(folder="test", filename="MC Test")
melody, comp2 = io.load_song(folder="test", filename="HMM Test")

snd.play_both(melody=melody,
                comp=comp1,
                bpm=100)

snd.play_both(melody=melody,
                comp=comp2,
                bpm=100)