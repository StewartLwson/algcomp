from .cellularautomata import Cellular_Automata
import numpy as np
import operator

class Genetic_Algorithm:
    def __init__(self, scale, generations = 5, population_size = 20, best_sample = 2, lucky_few = 1, npb = 4, chance = 50):
        self.scale = scale
        self.npb = npb
        self.population_size = population_size
        self.population = self.generate_first_population(self.npb)
        self.best_sample = best_sample
        self.lucky_few = lucky_few
        for _ in range(generations):
            self.parents = self.tournament_selection(self.population)
            self.population = self.multipoint_crossover(self.parents)
            self.mutate(self.population, chance)
        self.sort_population()


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
            if v == "-":
                for x in range(0, self.npb):
                    if c + x < len(melody):
                        if melody[c + x] == "-":
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

    def sort_population(self):
        sorted_population = {}
        for sequence in self.population:
            sorted_population[str(sequence)] = self.fitness(sequence)
        sorted_population = sorted(sorted_population.items(), key = operator.itemgetter(1), reverse = True)
        return sorted_population

    # Selects the best individuals in a population plus a lucky few
    def best_selection(self):
        sorted_population = {}
        next_gen = []
        for sequence in self.population:
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
        winners = []
        if len(population) % 2 != 0:
            #winners.append(population[len(population) - 1])
            del population[len(population) - 1]
        tournaments = [population[x:x+2] for x in range(0, len(population), 2)]

        for tournament in tournaments:
            fitness1 = self.fitness(tournament[0])
            fitness2 = self.fitness(tournament[1])
            best_score = max(fitness1, fitness2)
            if fitness1 == best_score:
                winners.append(tournament[0])
                print("Winner: " + str(tournament[0]))
            else:
                winners.append(tournament[1])
                print("Winner: " + str(tournament[1]))
        return winners

    def singlepoint_crossover(self, winners):
        leftover = []
        if len(winners) % 2 == 0:
            children = winners
        else:
            children = winners[:len(winners) - 2]
            leftover = winners[len(winners) - 1]
        point = np.random.randint(1, 10)
        parents = [winners[x:x+2] for x in range(0, len(winners), 2)]

        for couple in parents:
            for c, _ in enumerate(couple):
                split1 = couple[c % 2][0:point]
                split2 = couple[(c + 1) % 2][point:12*self.npb]
                print(str(split1 + split2))
        children + leftover
        print("Next generation: " + str(children))
        return children

    def multipoint_crossover(self, winners):
        leftover = []
        if len(winners) % 2 == 0:
            children = winners
        else:
            children = winners[:len(winners) - 2]
            leftover = winners[len(winners) - 1]
        parents = [winners[x:x+2] for x in range(0, len(winners), 2)]

        for couple in parents:
            child1 = []
            child2 = []
            for x in range(0, len(couple[0]), self.npb):
                chance = np.random.randint(0, 1)
                if chance == 0:
                    child1 = child1 + couple[0][x:x+self.npb]
                    child2 = child2 + couple[1][x:x+self.npb]
                else:
                    child1 = child1 + couple[1][x:x+self.npb]
                    child2 = child2 + couple[0][x:x+self.npb]
            children.append(child1)
            children.append(child2)
        children + leftover
        return children


    def mutate(self, population, chance):
        index = np.random.randint(0, 11)
        for individual in population:
            if np.random.randint(0, 100) < chance:
                individual[index] = np.random.choice(self.scale)

    def get_individuals(self, size):
        individuals = []
        for i in range(size):
            individuals.append(self.population[i])
        return individuals




