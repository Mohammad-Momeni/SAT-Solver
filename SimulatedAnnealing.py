import math
import random
import matplotlib.pyplot as plt
from pysat.formula import CNF
from pysat.solvers import Solver

def makeFirstSolution(size):
    firstSolution = []
    for i in range(1, size+1):
        value = (random.randint(0, 1))
        if value == 1:
            firstSolution.append(i)
        else:
            firstSolution.append(-i)
    return firstSolution

def makeNewSolution(currentSolution):
    newSolution = currentSolution.copy()
    index = (random.randint(0, len(currentSolution) - 1))
    newSolution[index] = -newSolution[index]
    return newSolution

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

def simulatedAnnealing(formula):
    data = []
    hasSolution = False
    solver = Solver()
    solver.append_formula(formula.clauses)
    if solver.solve():
        hasSolution = True
    solver.delete()
    currentSolution = makeFirstSolution(formula.nv)
    currentSolutionEvaluation = evaluation(currentSolution, formula)
    T = 100000000
    notChanged = 0
    solutionCounter = 0
    data.append((solutionCounter, currentSolutionEvaluation))
    while notChanged < 10000 and currentSolutionEvaluation < len(formula.clauses):
        newSolution = makeNewSolution(currentSolution)
        newSolutionEvaluation = evaluation(newSolution, formula)
        if newSolutionEvaluation > currentSolutionEvaluation:
            currentSolution = newSolution
            notChanged = 0
        else:
            p = math.exp(-abs((newSolutionEvaluation - currentSolutionEvaluation))/T)
            value = random.uniform(0, 1)
            if value < p:
                currentSolution = newSolution
                if newSolutionEvaluation != currentSolutionEvaluation:
                    notChanged = 0
            else:
                notChanged += 1
        T = T * 0.95
        if notChanged == 0:
            currentSolutionEvaluation = evaluation(currentSolution, formula)
        print('Iteration: ', solutionCounter, ' Evaluation: ', currentSolutionEvaluation)
        solutionCounter += 1
        data.append((solutionCounter, currentSolutionEvaluation))
    return hasSolution, currentSolution, currentSolutionEvaluation, data

def plot(data):
    x = [data[i][0] for i in range(len(data))]
    y = [data[i][1] for i in range(len(data))]
    plt.figure()
    plt.plot(x, y)
    plt.xlabel('Number of Iterations')
    plt.ylabel('Number of Satisfied Clauses')
    plt.title('Simulated Annealing')
    plt.show()

def main(filename):
    formula = CNF(from_file=filename)
    hasSolution, solution, solutionEvaluation, data = simulatedAnnealing(formula)
    if hasSolution:
        print('Satisfiable\nBest Found Solution: ', solution, '\nNumber of Satisfied Clauses: ', solutionEvaluation)
    else:
        print('Unsatisfiable\nBest Possible Found Solution: ', solution, '\nNumber of Satisfied Clauses: ', solutionEvaluation)
    plot(data)

if __name__ == '__main__':
    main('SATs/Input.cnf')