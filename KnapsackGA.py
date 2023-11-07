from knapsack import *
import random

def generatePopulation(size, items):
    population = []
    genes = [0, 1]
    for i in range(size):
        chromosome = []
        for j in range(len(items.weights)):
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

    for i in range(len(generation)):
        fitnesses.append([claculateFitness(generation[i], knapsack), i])

    sorted(fitnesses, key=lambda x: x[1], reverse=True)
    sum = 0

    for i in range(len(fitnesses)):
        fitnesses[i][0] = i + 1
        sum += i + 1

    for i in range(len(fitnesses)):
        fitnesses[i][0] = fitnesses[i][0] / sum
        if i > 0:
            fitnesses[i][0] += fitnesses[i - 1][0]

    selected_parents = []
    for i in range(n):
        rn = random.random()
        for j in range(len(fitnesses)):
            if rn < fitnesses[j][0]:
                selected_parents.append(generation[fitnesses[j][1]])
                break

    return selected_parents


def crossover(parent1, parent2):
    crossoverPoint = random.randint(0, len(parent1) - 1)
    child1 = parent1[0:crossoverPoint] + parent2[crossoverPoint:]
    child2 = parent2[0:crossoverPoint] + parent1[crossoverPoint:]
    return child1, child2


def mutate(chromosome):
    Mc = 0.05
    for i in range(len(chromosome)):
        rn = random.random()
        if rn < Mc:
            chromosome[i] = not chromosome[i]

    return chromosome


def replace(population, child1, child2):
    return population[2:] + [child1, child2]


if __name__ == "__main__":
    ks = knapsack(  values=[1, 15, 30, 10, 50],
                    weights=[4, 5, 6, 19, 2],
                    capacity=15)

    numGenerations = 100
    populationSize = 50
    Cp = 0.3
    initial_population = generatePopulation(populationSize, ks)

    BestSolution = None
    bestFitness = float("-inf")

    for generation in range(numGenerations):
        selectedParents = selection(initial_population, ks)

        newGeneration = []

        for i in range(0, populationSize, 2):
            rn = random.random()
            parent1 = selectedParents[i]
            parent2 = selectedParents[i + 1]
            if rn < Cp:
                child1, child2 = crossover(parent1, parent2)
                newGeneration.append(child1)
                newGeneration.append(child2)
            else:
                newGeneration.append(parent1)
                newGeneration.append(parent2)

        for i in range(len(newGeneration)):
            newGeneration[i] = mutate(newGeneration[i])

        initial_population = newGeneration

        generationFitness = [claculateFitness(chromosome, ks) for chromosome in initial_population]

        maxFitness = max(generationFitness)
        if maxFitness > bestFitness:
            bestFitness = maxFitness
            BestSolution = initial_population[generationFitness.index(maxFitness)]

    print(BestSolution)
    print(bestFitness)
