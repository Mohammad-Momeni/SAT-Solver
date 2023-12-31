import random
import matplotlib.pyplot as plt
from pysat.formula import CNF
from pysat.solvers import Solver

def makeRandomSolution(size):
    randomSolution = []
    for i in range(1, size+1):
        value = (random.randint(0, 1))
        if value == 1:
            randomSolution.append(i)
        else:
            randomSolution.append(-i)
    return randomSolution

def evaluation(solution, formula):
    nofCorrect = 0
    parentheses = formula.clauses
    for parenthesis in parentheses:
        flag = False
        for value in parenthesis:
            if value in solution:
                flag = True
        if flag:
            nofCorrect += 1
    return nofCorrect

def generationEvaluation(currentGeneration):
    max = -1
    maxIndex = -1
    for i in range(len(currentGeneration)):
        if currentGeneration[i][1] > max:
            max = currentGeneration[i][1]
            maxIndex = i
    return maxIndex, max

def makeFirstGeneration(formula):
    firstGeneration = []
    for i in range(0, 100):
        newSolution = makeRandomSolution(formula.nv)
        newSolutionEvaluation = evaluation(newSolution, formula)
        firstGeneration.append((newSolution, newSolutionEvaluation))
    return firstGeneration

def calculateProbabilities(currentGeneration):
    totalEvaluation = sum(currentGeneration[i][1] for i in range(len(currentGeneration)))
    probabilities = [currentGeneration[i][1] / totalEvaluation for i in range(len(currentGeneration))]
    return probabilities

def transformToBinary(solution):
    binary = []
    for i in range(len(solution)):
        if solution[i] > 0:
            binary.append(1)
        else:
            binary.append(0)
    return binary

def crossover(parent1, parent2):
    binary1 = transformToBinary(parent1)
    binary2 = transformToBinary(parent2)
    value1 = (random.randint(0, len(binary1) - 1))
    value2 = (random.randint(0, len(binary1) - 1))
    if value1 > value2:
        value1, value2 = value2, value1
    newBinary1 = binary1[:value1] + binary2[value1:value2] + binary1[value2:]
    newBinary2 = binary2[:value1] + binary1[value1:value2] + binary2[value2:]
    child1 = []
    child2 = []
    for i in range(len(newBinary1)):
        if newBinary1[i] == 1:
            child1.append(i+1)
        else:
            child1.append(-(i+1))
        if newBinary2[i] == 1:
            child2.append(i+1)
        else:
            child2.append(-(i+1))
    return child1, child2

def mutation(solution):
    newSolution = solution.copy()
    index1 = (random.randint(0, len(solution) - 1))
    index2 = (random.randint(0, len(solution) - 1))
    newSolution[index1] = -newSolution[index1]
    if index1 != index2:
        newSolution[index2] = -newSolution[index2]
    return newSolution

def makeNewGeneration(currentGeneration, formula):
    newGeneration = []
    probabilities = calculateProbabilities(currentGeneration)
    nofNewSolutions = 0
    while nofNewSolutions < len(currentGeneration):
        parent1, parent2 = random.choices(currentGeneration, weights=probabilities, k=2)
        if random.uniform(0, 1) < 0.8:
            child1, child2 = crossover(parent1[0], parent2[0])
            nofNewSolutions += 2
            if random.uniform(0, 1) < 0.01:
                child1 = mutation(child1)
            if random.uniform(0, 1) < 0.01:
                child2 = mutation(child2)
            child1Evaluation = evaluation(child1, formula)
            child2Evaluation = evaluation(child2, formula)
            newGeneration.append((child1, child1Evaluation))
            newGeneration.append((child2, child2Evaluation))
    return newGeneration

def standardGeneticAlgorithm(formula):
    data = []
    hasSolution = False
    solver = Solver()
    solver.append_formula(formula.clauses)
    if solver.solve():
        hasSolution = True
    solver.delete()
    currentGeneration = makeFirstGeneration(formula)
    currentMaxIndex, currentGenerationEvaluation = generationEvaluation(currentGeneration)
    generationCounter = 0
    data.append((generationCounter, currentGenerationEvaluation))
    while generationCounter <= 1000 and currentGenerationEvaluation < len(formula.clauses):
        newGeneration = makeNewGeneration(currentGeneration, formula)
        newMaxIndex, newGenerationEvaluation = generationEvaluation(newGeneration)
        currentGeneration = newGeneration
        currentMaxIndex = newMaxIndex
        currentGenerationEvaluation = newGenerationEvaluation
        print('Generation: ', generationCounter, ' Max Evaluation: ', currentGenerationEvaluation)
        generationCounter += 1
        data.append((generationCounter, currentGenerationEvaluation))
    return hasSolution, currentGeneration[currentMaxIndex], data

def plot(data):
    x = [data[i][0] for i in range(len(data))]
    y = [data[i][1] for i in range(len(data))]
    plt.figure()
    plt.plot(x, y)
    plt.xlabel('Generation')
    plt.ylabel('Number of Satisfied Clauses')
    plt.title('Standard Genetic Algorithm')
    plt.show()

def main(filename):
    formula = CNF(from_file=filename)
    hasSolution, solution, data = standardGeneticAlgorithm(formula)
    if hasSolution:
        print('Satisfiable\nBest Found Solution: ', solution[0], '\nNumber of Satisfied Clauses: ', solution[1])
    else:
        print('Unsatisfiable\nBest Possible Found Solution: ', solution[0], '\nNumber of Satisfied Clauses: ', solution[1])
    plot(data)

if __name__ == '__main__':
    main('SATs/Input.cnf')