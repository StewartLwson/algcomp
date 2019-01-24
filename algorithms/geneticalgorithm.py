from .cellularautomata import Cellular_Automata
import numpy as np
import operator

class Genetic_Algorithm:
    def __init__(self, scale, population_size = 5, best_sample = 2, lucky_few = 1):
        self.scale = scale
        self.population_size = population_size
        self.first_population = self.generate_first_population()
        self.best_sample = best_sample
        self.lucky_few = lucky_few

    def fitness(self, melody):
        score = 0
        for c, v in enumerate(melody):
            if c == 0:
                if v == 0:
                    score += 1
                else:
                    score -= 1
            if c == len(melody) - 1:
                if v == 0:
                    score += 1
                else:
                    score -= 1
                if v == 6:
                    score -= 1
            if v == 6 and c < len(melody) - 1:
                if melody[c + 1] == 5 or melody[c + 1] == 7 or melody[c - 1] == 5 or melody[c - 1] == 7:
                    score += 1
                else:
                    score -= 1
        if score == 0:
            return 0
        elif score > 0:
            return 1 - (1 / score)
        else:
            return -1 - (1 / score)

    def generate_first_population(self):
        population = []
        ca = Cellular_Automata()
        for _ in range(self.population_size):
            melody = ca.generate_melody(self.scale, bars = 12, npb = 1)
            population.append(melody)
        return population

    def selection(self):
        sorted_population = {}
        next_gen = []
        for sequence in self.first_population:
            sorted_population[str(sequence)] = self.fitness(sequence)
        sorted_population = sorted(sorted_population.items(), key = operator.itemgetter(1), reverse = True)
        print(sorted_population)
        for i in range(self.best_sample):
            next_gen.append(sorted_population[i][0])
        for i in range(self.lucky_few):
            next_gen.append(sorted_population[np.random.randint(self.best_sample, self.population_size - 1)][0])
        np.random.shuffle(next_gen)
        return next_gen





