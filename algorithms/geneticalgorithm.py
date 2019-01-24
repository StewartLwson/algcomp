class Genetic_Algorithm:
    def __init__(self):
        pass

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
        print(score)
        if score == 0:
            return 0
        elif score > 0:
            return 1 - (1 / score)
        else:
            return -1 - (1 / score)




