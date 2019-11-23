import numpy as np
import random
import csv

with open('file.csv') as f:
    DataSet = [tuple(line) for line in csv.reader(f)]

POP_SIZE = 9
REMAINING_HOURS = 6
ELITES_NUMBER = 3
WANTED_MARK = 12
MAX_GEN = 30

# chromosome class:


class Chromosome:

    def __init__(self):
        self.genes = np.random.randint(2, size=len(DataSet))
        self.fitness = 0
        self.volume = 0
        # Check if the volume is greater than the remaining hours then flip a random bit that equal 1 to 0
        while (self.get_volume() > REMAINING_HOURS):
            self.genes[np.random.choice(np.where(self.genes == 1)[0])] = 0

    def get_genes(self):
        return self.genes

    def __str__(self):
        return self.genes.__str__()

    def get_fitness(self):
        self.fitness = 0
        for (selected, (_, _, mark)) in zip(self.genes, DataSet):
            if selected == 1:
                self.fitness += int(mark)
        return self.fitness

    def get_volume(self):
        self.volume = 0
        for (selected, (_, required_time, _)) in zip(self.genes, DataSet):
            if selected == 1:
                self.volume += int(required_time)
        return self.volume


def roulette_wheel_selection(pop):
    partialSum = 0
    sumFitness = 0
    for i in range(POP_SIZE):
        sumFitness += pop[i].get_fitness()
        randomShot = random.random() * sumFitness
        i = -1
    while partialSum < randomShot and i < POP_SIZE-1:
        i += 1
        partialSum += pop[i].get_fitness()
    return pop[i]


def tour_selection(pop):
    selected = np.empty(4, dtype=Chromosome)
    i = 0
    while i < 3:
        selected[i] = pop[random.randint(0, POP_SIZE-1)]
        i += 1
    i = 1
    highest_fitness = 0
    while i < 3:
        if selected[i].get_fitness() > selected[highest_fitness].get_fitness():
            highest_fitness = i
        i += 1
    return selected[highest_fitness]


def crossover(parent1, parent2):
    cp = random.randint(0, len(parent1.genes)-1)
    p1 = parent1.genes[:cp]
    p2 = parent2.genes[cp:]
    child = Chromosome()
    child.genes = np.concatenate((p1, p2), axis=None)
    return child


def mutation(child):
    index = child.genes[np.random.choice(child.genes)]
    if (child.genes[index] == 1):
        child.genes[index] = 0
    else:
        child.genes[index] = 1


def repair(child):
    while (child.get_volume() > REMAINING_HOURS):
        child.genes[np.random.choice(np.where(child.genes == 1)[0])] = 0


def sort_population(pop):
    pop_fitness = np.empty(POP_SIZE)
    for i in range(POP_SIZE):
        pop_fitness[i] = pop[i].get_fitness()
    inds = pop_fitness.argsort()[::-1][:POP_SIZE]
    sorted_pop = pop[inds]
    return sorted_pop


def evolve(pop):

    parent_1 = roulette_wheel_selection(pop)
    parent_2 = roulette_wheel_selection(pop)
    parent_3 = roulette_wheel_selection(pop)

    # parent_1 = tour_selection(pop)
    # parent_2 = tour_selection(pop)
    # parent_3 = tour_selection(pop)

    child_1 = crossover(parent_1, parent_2)
    child_2 = crossover(parent_2, parent_1)
    child_3 = crossover(parent_1, parent_3)
    child_4 = crossover(parent_3, parent_1)
    child_5 = crossover(parent_3, parent_2)
    child_6 = crossover(parent_2, parent_3)

    mutation(child_1)
    mutation(child_2)
    mutation(child_3)
    mutation(child_4)
    mutation(child_5)
    mutation(child_6)

    repair(child_1)
    repair(child_2)
    repair(child_3)
    repair(child_4)
    repair(child_5)
    repair(child_6)

    new_pop = np.array([child_1, child_2,
                        child_3, child_4, child_5, child_6])
    new_pop = np.concatenate((pop[:ELITES_NUMBER], new_pop), axis=None)

    return sort_population(new_pop)


def print_pop(pop):
    for i in range(np.size(pop, 0)):
        print(pop[i].get_genes())


def final_result(chromosome):
    result = ''
    for (selected, (chapter, _, _)) in zip(chromosome, DataSet):
        if selected == 1:
            result = result + chapter + ','

    return result


# main
generation_number = 0
population = np.array([Chromosome() for _ in range(POP_SIZE)])
population = sort_population(population)
print_pop(population)
print("-------")
print("generation number is:", generation_number)
while population[0].get_fitness() < WANTED_MARK and generation_number < MAX_GEN:
    population = evolve(population)
    generation_number += 1
    print("----------------------------------------------")
    print_pop(population)
    print("-------")
    print("generation number is:", generation_number)
    print("-------")
    print("best fitness:", population[0].get_fitness())

print("********final result**********")
print("chapters to study:", final_result(population[0].genes))
