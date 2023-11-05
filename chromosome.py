def generatePopulation(size, items):
    population = []
    genes = [0, 1]
    for i in range(size):
        chromosome = []
        for j in range(len(items)):
            chromosome.append(random.choice(genes))
        population.append(chromosome)
    return population

def claculateFitness(chromosome):
    