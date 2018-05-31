from Entity import *
from random import randint

POPULATION_SIZE = 100
GENERATIONS_NUMBER = 100
SELECTION_RATE = .5
CROSSOVER_RATE = 0
MUTATION_RATE = 0.1


def run(distances, flows):
    output = open('./data/result.csv', 'w')
    output.write('generation;best score;average score;worst score\n')
    population = generate(POPULATION_SIZE, len(distances))

    for generation in range(GENERATIONS_NUMBER):
        if len(population) < POPULATION_SIZE:
            new_population = generate(POPULATION_SIZE - len(population), len(distances))
            population.extend(new_population)
        max_score, avg_score, min_score, best_entity_id = evaluation(population, distances, flows)
        output.write(str(generation) + ';' + str(max_score).replace('.', ',') + ';' +
                     str(avg_score).replace('.', ',') + ';' + str(min_score).replace('.', ',') + '\n')
        best_entity = population.pop(best_entity_id)
        selection(population)
        crossover(population)
        mutation(population)
        population.append(best_entity)

    output.close()


def generate(number_of_entities, number_of_genes):
    out_population = []
    for i_entity in range(number_of_entities):
        out_population.append(Entity(number_of_genes))
    return out_population


def selection(population):
    winners = []
    number_of_selected = int(len(population) * SELECTION_RATE * 0.5)
    for i in range(number_of_selected):
        entity1 = population.pop(randint(0, len(population)-1))
        entity2 = population.pop(randint(0, len(population)-1))
        if entity1.score < entity2.score:
            winners.append(entity2)
        else:
            winners.append(entity1)
    population.extend(winners)


def crossover(population):
    childs = []
    parents = []
    for i in range(int(len(population)/2)):
        if randint(0, 100) < CROSSOVER_RATE * 100:
            parent1 = population.pop(randint(0, len(population) - 1))
            parent2 = population.pop(randint(0, len(population) - 1))
            parents.append(parent1)
            parents.append(parent2)
            child = Entity(len(parent1.genes))
            cross_point = randint(1, len(parent1.genes) - 1)
            child.genes = parent1.genes[:cross_point]
            child.genes.extend(parent2.genes[cross_point:])
            unique_child_genes = []
            for idx, gene in enumerate(child.genes):
                if gene not in unique_child_genes:
                    unique_child_genes.append(gene)
                if idx not in child.genes:
                    unique_child_genes.append(idx)
            child.genes = unique_child_genes
            childs.append(child)

    population.extend(childs)
    # population.extend(parents)


def mutation(population):
    for entity in population:
        if randint(0, 100) < MUTATION_RATE * 100:
            entity.mutate()


def evaluation(population, distances, flows):
    max_score = 9999999999
    min_score = 0
    full_score = 0
    best_entity = 0
    for entity_i, entity in enumerate(population):
        cur_score = entity.evaluate(distances, flows)
        if cur_score < max_score:
            max_score = cur_score
            best_entity = entity_i
        if cur_score > min_score:
            min_score = cur_score
        full_score += cur_score
    avg_score = full_score/len(population)
    normalize(population)
    return max_score, avg_score, min_score,best_entity


def normalize(population):
    scores = []
    for ent in population:
        scores.append(ent.score)
    score_sum = sum(scores)
    norm = [float(i) / score_sum for i in scores]
    for id, ent in enumerate(population):
        ent.normalized_score = norm[id]