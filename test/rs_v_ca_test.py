from util.sound import Sound
from util.io import IO
from util.musicgenerator import MusicGenerator
from algorithms.geneticalgorithm import Genetic_Algorithm

io = IO()
snd = Sound()
gen = MusicGenerator()

scales = io.load_scales()
chromatic = scales["chromatic"]["C"]
major = scales["major"]["C"]

ga = Genetic_Algorithm(scale=chromatic, style="jazz", other_scale=major)

rs_fitnesses = []
for i in range(0, 255):
    print(i + 1)
    melody = gen.generate_jazz_melody("C", 16, 8, "RS", chromatic=True)
    rs_fitnesses.append(ga.fitness(melody, chromatic, "jazz", major))

rs_fitness_average = sum(rs_fitnesses) / len(fs_ritnesses)
print(rs_fitness_average)

good_rs = []
good_rs_fitnesses = []
for i, fitness in enumerate(rs_fitnesses):
    if fitness > rs_fitness_average:
        good_rs.append(i)
        good_rs_fitnesses.append(fitness)

print(good_rs)
print(good_rs_fitnesses)


fitnesses = []
for i in range(0, 255):
    print(i + 1)
    melody = gen.generate_jazz_melody("C", 16, 8, "CA", rule=i, change_rule=False, chromatic=True)
    fitnesses.append(ga.fitness(melody, chromatic, "jazz", major))
