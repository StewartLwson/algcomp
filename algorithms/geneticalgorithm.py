#!/usr/bin/env python

from algorithms.cellularautomata import Cellular_Automata
import numpy as np
import operator

class Genetic_Algorithm:
    """
    A Genetic Algorithm that evolves musical sequences according to a fitness
    that describes a specific style.

    Parameters
    ----------
        scale: list
            The scale degrees in which the generated sequences are derived.
        style: str
            The style in which the sequences will be evaluated.
        generations: int, optional
            The amount of times the evolutionary process will iterate.
        population_size: int, optional
            The amount of sequences that will be generate for the initial
            population.
        best_sample: int, optional
            The cutoff size for fittest individuals when using best selection.
        lucky_few: int, optional
            The amount of lucky individuals to be chosen from outside the
            best sample when using best selection.
        rule: int, optional
            The rule given to the Cellular Automata when generating the
            initial population.
        npb: int, optional
            The maximum amount of notes allowed in each bar of a sequence.
        chance: int, optional
            The chance a mutation will occur when generating children.

    """
    def __init__(self, scale, style, generations = 5, population_size = 20,
    best_sample = 8, lucky_few = 2, rule = 150, bars = 1, npb = 4, chance = 50):
        self.scale = scale
        self.style = style
        self.npb = npb
        self.rule = rule
        self.population_size = population_size
        self.population = self.generate_first_population(scale, bars, npb, rule)
        self.best_sample = best_sample
        self.chance = chance
        self.lucky_few = lucky_few
        for _ in range(generations):
            self.parents = self.tournament_selection(self.population)
            self.population = self.multipoint_crossover(self.parents)
        self.sort_population()

    def get_population(self):
        """
        Returns the current population.

        """
        return self.population

    def musical_fitness(self, scale, melody):
        """
        Returns a fitness score based on general music theory concepts. A
        higher score is given to sequences that start and end on root notes
        and sequences that play do not have rests on strong beats.

        Parameters
        ----------

            melody: list
                The melodic sequence that is being scored by the fitness
                function.
        """
        score = 0
        for c, v in enumerate(melody):
            if c == 0: # on first note of the sequence
                score += 1 if v == scale[0] else -1 # check if note is root
            if c == len(melody) - 1: # on last note of sequence
                score += 1 if v == scale[0] else -1 # check if note is root
            if c % 2 == 0: # on strong beats
                score += 1 if v != "-" else -1 # check if note is rest
        return score

    def blues_fitness(self, scale, melody):
        """
        Returns a fitness score based on blues specific syntax. A higher score
        is given when the blues note is played correctly (inbetween the 4th
        and 5th and not at the start and end of a sequence).

        Parameters

            melody: list
                The melodic sequence that is being scored by the fitness
                function.

        """
        score = 0
        for c, v in enumerate(melody):
            if c == 0:
                score += 1 if v != scale[3] else -1
            if c == len(melody) - 1:
                score += 1 if v != scale[3] else -1
            if v == scale[3] and c < len(melody) - 1:
                if melody[c + 1] == scale[2] or melody[c + 1] == scale[4] or \
                melody[c - 1] == scale[2] or melody[c - 1] == scale[4]:
                    score += 1
                else:
                    score -= 1
        return score

    def fitness(self, scale, melody, style):
        """
        Returns a fitness for a given melody based score given by the
        fitness sub-functions. This total score is then normalized
        between -1 and 1.

        Parameters
        ----------
            melody: list
                The melodic sequence that is being scored by the fitness
                function.
            style: string
                The style of the sequence so that its fitness can be scored
                correctly.

        """
        score = 0
        score += self.musical_fitness(scale, melody) * 100
        if style == "blues":
            score += self.blues_fitness(scale, melody)

        normalized_score = 0
        if score > 0:
            normalized_score = 1 - (1 / score)
        elif score < 0:
            normalized_score = -1 - (1 / score)
        return normalized_score

    def generate_first_population(self, scale, bars, npb, rule):
        """
        Returns an initial population to be evolved by the Genetic Algorithm.

        Parameters
        ----------
            npb: int
                The maximum amount of notes allowed in each bar of a sequence.
            rule: int
                The rule given to the Cellular Automata when generating the
                initial population.

        """
        population = []
        ca = Cellular_Automata()
        for _ in range(self.population_size):
            melody = ca.generate_melody(scale, bars, npb)
            population.append(melody)
        return population

    def sort_population(self):
        """
        Returns a population of musical sequences sorted ascendingly by their
        fitness.

        """
        sorted_population = {}
        for sequence in self.population:
            sorted_population[str(sequence)] = self.fitness(scale = self.scale, melody = sequence, style = self.style)
        sorted_population = sorted(sorted_population.items(), key = operator.itemgetter(1), reverse = True)
        return sorted_population

    def best_selection(self, population):
        """
        Returns a sample of the fittest individuals in a population and a
        random amount of lucky individuals outside of the fittest.

        """
        leftover = []
        if len(population) % 2 != 0:
            population = population[:len(population) - 1]
            leftover = population[len(population) - 1]

        sorted_population = {}
        next_gen = []
        for sequence in population:
            sorted_population[str(sequence)] = self.fitness(scale = self.scale, melody = sequence, style = self.style)
        sorted_population = sorted(sorted_population.items(), key = operator.itemgetter(1), reverse = True)
        for i in range(self.best_sample):
            next_gen.append(sorted_population[i][0])
        for i in range(self.lucky_few):
            next_gen.append(sorted_population[np.random.randint(self.best_sample, self.population_size - 1)][0])
        next_gen.append(leftover)
        np.random.shuffle(next_gen)
        return next_gen

    def tournament_selection(self, population):
        """
        Returns a sample of individuals chosen by splitting the population
        into subgroups of two and selecting the fittest in the subgroup.

        Parameters
        ----------
            population: list
                The population of musical sequences to be selected from.

        """
        winners = []
        leftover = []
        if len(population) % 2 != 0:
            population = population[:len(population) - 1]
            leftover = population[len(population) - 1]
        tournaments = [population[x:x+2] for x in range(0, len(population), 2)]

        for tournament in tournaments:
            fitness1 = self.fitness(scale = self.scale, melody = tournament[0], style = self.style)
            fitness2 = self.fitness(scale = self.scale, melody = tournament[1], style = self.style)
            best_score = max(fitness1, fitness2)
            if fitness1 == best_score:
                winners.append(tournament[0])
            else:
                winners.append(tournament[1])
        winners.append(leftover)
        return winners

    def singlepoint_crossover(self, winners):
        """
        Returns the next generation of a population by crossing over pairs
        of individuals in the current population at a single random point and
        appending their two children to the population.

        Parameters
        ----------
            winners: list
                The selected individuals who will be crossed over.

        """
        leftover = []
        if len(winners) % 2 == 0:
            children = winners
        else:
            children = winners[:len(winners) - 1]
            leftover = winners[len(winners) - 1]
        point = np.random.randint(1, 10)
        parents = [winners[x:x+2] for x in range(0, len(winners), 2)]

        for couple in parents:
            for c, _ in enumerate(couple):
                split1 = couple[c % 2][0:point]
                split2 = couple[(c + 1) % 2][point:12*self.npb]
                child = split1 + split2
                child = self.mutate(child, self.chance)
                children.append(child)
        children.append(leftover)
        return children

    def multipoint_crossover(self, winners):
        """
        Returns the next generation of a population by crossing over pairs
        of individuals in the current population at multiple points defined
        to be at the beginning of each bar.

        Parameters
        ----------
            winners: list
                The selected individuals who will be crossed over.
        """
        leftover = []
        if len(winners) % 2 != 0:
            winners = winners[:len(winners) - 1]
            leftover = winners[len(winners) - 1]
        parents = [winners[x:x+2] for x in range(0, len(winners), 2)]

        children = winners
        for couple in parents:
            child1 = []
            child2 = []
            for x in range(0, len(couple[0]), self.npb):
                chance = np.random.randint(0, 2)
                if chance == 0:
                    child1 = child1 + couple[0][x:x+self.npb]
                    child2 = child2 + couple[1][x:x+self.npb]
                else:
                    child1 = child1 + couple[1][x:x+self.npb]
                    child2 = child2 + couple[0][x:x+self.npb]
            children.append(child1)
            children.append(child2)
        children.append(leftover)
        return children

    def mutate(self, individual, chance):
        """
        Returns an individual that may have had a random note replaced
        depending on a given chance.

        Parameters
        ----------
            individual: list
                The sequence that is being mutated.
            chance: int
                The chance that the mutation will occur.

        """
        index = np.random.randint(0, 11)
        if np.random.randint(0, 100) < chance:
            individual[index] = np.random.choice(self.scale)
        return individual




