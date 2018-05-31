import random


class Entity(object):
    def __init__(self, number_of_genes):
        self.genes = []
        self.score = 0
        self.normalized_score = 0
        for i in range(number_of_genes):
            self.genes.append(i)

        random.shuffle(self.genes)

    def mutate(self):
        position1 = random.randint(0, len(self.genes)-1)
        position2 = random.randint(0, len(self.genes)-1)
        while  position2 == position1:
            position2 = random.randint(0, len(self.genes) - 1)
        self.genes[position1], self.genes[position2] = self.genes[position2], self.genes[position1]

    def evaluate(self, distances, flows):
        if self.score == 0:
            for loc_idx_f in range(len(distances)):
                fac_und_loc_f = self.genes[loc_idx_f]
                for loc_idx_s in range(0, len(distances)):
                    fac_und_loc_s = self.genes[loc_idx_s]
                    self.score += int(flows[fac_und_loc_f][fac_und_loc_s]) * int(distances[loc_idx_f][loc_idx_s])
            self.score = self.score / 2.
        return self.score