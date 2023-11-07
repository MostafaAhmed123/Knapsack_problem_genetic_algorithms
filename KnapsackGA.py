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


def calculateFitness(chromosome, knapsack):
    sumOfWeights = 0
    sumOfValues = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            sumOfWeights += knapsack.weights[i]
            sumOfValues += knapsack.values[i]

    if sumOfWeights > knapsack.capacity:
        return 0

    return sumOfValues


def selection(generation, knapsack):
    fitnesses = []
    n = 10

    for i in range(len(generation)):
        fitness = calculateFitness(generation[i], knapsack)
        fitnesses.append([fitness, i])

    fitnesses.sort(key=lambda x: x[0], reverse=True)

    total_fitness = sum(fitness for fitness, _ in fitnesses)
    cumulative_fitness = 0

    for i in range(len(fitnesses)):
        cumulative_fitness += fitnesses[i][0]
        fitnesses[i][0] = cumulative_fitness / total_fitness

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
            chromosome[i] = 1 - chromosome[i]
    return chromosome


def replacement(population, size, knapsack):
    generationFitness = [
        calculateFitness(chromosome, knapsack) for chromosome in population
    ]

    population = [
        x
        for _, x in sorted(
            zip(generationFitness, population), key=lambda pair: pair[0], reverse=True
        )
    ]

    population = population[0:size]
    return population


def GA(ks):
    numGenerations = 100
    populationSize = 100
    Cp = 0.7
    initial_population = generatePopulation(populationSize, ks)

    BestSolution = None
    bestFitness = 0

    for generation in range(numGenerations):
        selectedParents = selection(initial_population, ks)

        newGeneration = []

        for i in range(0, len(selectedParents), 2):
            rn = random.random()
            parent1 = selectedParents[i]
            parent2 = selectedParents[i + 1]
            if rn < Cp:
                child1, child2 = crossover(parent1, parent2)
                newGeneration.append(child1)
                newGeneration.append(child2)

        for i in range(len(newGeneration)):
            newGeneration[i] = mutate(newGeneration[i])

        initial_population.extend(newGeneration)

        initial_population = replacement(initial_population, populationSize, ks)

        generationFitness = [
            calculateFitness(chromosome, ks) for chromosome in initial_population
        ]

        maxFitness = max(generationFitness)
        if maxFitness > bestFitness:
            bestFitness = maxFitness
            BestSolution = initial_population[generationFitness.index(maxFitness)]

    return BestSolution, bestFitness


if __name__ == "__main__":
    Input = input("enter the file name with .txt extension: ")
    with open(Input, "r") as file:
        num_test_cases = int(file.readline().strip())
        i = 0
        while i < num_test_cases:
            line = file.readline().strip()
            if line != "":
                knapsack_size = int(line)
                line = file.readline().strip()
                num_items = int(line)
                weights = []
                values = []
                for _ in range(num_items):
                    weight, value = map(int, file.readline().split())
                    weights.append(weight)
                    values.append(value)
                ks = Knapsack(values, weights, knapsack_size)
                bestSolution, bestFitness = GA(ks)
                i += 1
                print("Test Case Number: ", i)
                print("Number of selected items = ", bestSolution.count(1))
                totalWeight = 0
                for j in range(len(bestSolution)):
                    if bestSolution[j] == 1:
                        totalWeight += weights[j]
                print("Total Value = ", bestFitness)
                print("Total weight = ", totalWeight)
                k = 0
                for j in range(len(bestSolution)):
                    if bestSolution[j] == 1:
                        k += 1
                        print("Item Number = ", k, " Weight = ", weights[j], end=" ")
                        print("Value = ", values[j])
