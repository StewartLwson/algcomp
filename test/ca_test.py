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

fitnesses = []
for i in range(0, 255):
    print(i + 1)
    melody = gen.generate_jazz_melody("C", 16, 8, "CA", rule=i, change_rule=False, chromatic=True)
    fitnesses.append(ga.fitness(melody, chromatic, "jazz", major))

fitness_average = sum(fitnesses) / len(fitnesses)
print(fitness_average)

good_rules = []
good_rules_fitnesses = []
for i, fitness in enumerate(fitnesses):
    if fitness > fitness_average:
        good_rules.append(i)
        good_rules_fitnesses.append(fitness)

print(good_rules)
print(good_rules_fitnesses)
