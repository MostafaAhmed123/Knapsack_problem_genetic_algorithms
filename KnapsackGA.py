from knapsack import *
import random

def generatePopulation(size, items):
    population = []
    genes = [0, 1]
    for i in range(size):
        chromosome = []
        for j in range(items.capacity):
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



if __name__ == "__main__":
    x = knapsack(3)
    x.weights.append(4)
    x.values.append(4)
    x.weights.append(5)
    x.values.append(5)
    x.weights.append(6)
    x.values.append(6)
    print(selection(generatePopulation(5, x), x))
