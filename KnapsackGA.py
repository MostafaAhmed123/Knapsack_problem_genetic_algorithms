from knapsack import *


def generatePopulation(size, items):
    population = []
    genes = [0, 1]
    for i in range(size):
        chromosome = []
        for j in range(len(items)):
            chromosome.append(random.choice(genes))
        population.append(chromosome)
    return population


def claculateFitness(chromosome, knapsack):
    sumOfWeights = 0
    sumOfValues = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            sumOfWeights += knapsack.weights[i]
            sumOfValues += knapsack.values[i]
    if sumOfWeights > knapsack.capacity:
        return -1
    return sumOfValues


# TODO cleanup that shit
def selection(generation, knapsack):
    fitnesses = []
    n = 10

    for solution in generation:
        fitnesses.append(claculateFitness(solution, knapsack))

    fitnesses.sort()
    rank = fitnesses
    sum = 0
    for i in range(len(rank)):
        rank[i] = i + 1
        sum += i + 1

    for i in range(len(rank)):
        rank[i] = rank[i] / sum
        if i > 0:
            rank[i] += rank[i - 1]

    selected_parents = []
    for i in range(n):
        rn = random.random()
        for j in range(len(rank)):
            if rn < rank[j]:
                selected_parents.append(generation[smth])
                break

    return selected_parents
