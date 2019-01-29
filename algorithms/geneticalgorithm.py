from .cellularautomata import Cellular_Automata
import numpy as np
import operator

class Genetic_Algorithm:
    def __init__(self, scale, population_size = 20, best_sample = 2, lucky_few = 1, npb = 1):
        self.scale = scale
        self.npb = npb
        self.population_size = population_size
        self.first_population = self.generate_first_population(self.npb)
        self.best_sample = best_sample
        self.lucky_few = lucky_few
        self.parents = self.tournament_selection(self.first_population)
        self.children = self.singlepoint_crossover(self.parents)

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

    def generate_first_population(self, npb):
        population = []
        ca = Cellular_Automata()
        for _ in range(self.population_size):
            melody = ca.generate_melody(self.scale, bars = 12, npb = npb)
            population.append(melody)
        return population

    # Selects the best individuals in a population plus a lucky few
    def best_selection(self):
        sorted_population = {}
        next_gen = []
        for sequence in self.first_population:
            sorted_population[str(sequence)] = self.fitness(sequence)
        sorted_population = sorted(sorted_population.items(), key = operator.itemgetter(1), reverse = True)
        for i in range(self.best_sample):
            next_gen.append(sorted_population[i][0])
        for i in range(self.lucky_few):
            next_gen.append(sorted_population[np.random.randint(self.best_sample, self.population_size - 1)][0])
        np.random.shuffle(next_gen)
        return next_gen

    # Selects the best individuals by splitting population into groups of two and
    # choosing fitter individual
    def tournament_selection(self, population):
        tournaments = [population[x:x+2] for x in range(0, len(population), 2)]
        winners = []
        for tournament in tournaments:
            fitness1 = self.fitness(tournament[0])
            fitness2 = self.fitness(tournament[1])
            best_score = max(fitness1, fitness2)
            if fitness1 == best_score:
                winners.append(tournament[0])
            else:
                winners.append(tournament[1])
        return winners

    def singlepoint_crossover(self, winners):
        point = np.random.randint(1, 10)
        parents = [winners[x:x+2] for x in range(0, len(winners), 2)]
        children = []
        for couple in parents:
            split1 = couple[0][0:point]
            print(split1)
            split2 = couple[1][point:12]
            print(split2)
            child = split1 + split2
            children.append(child)
        return children




