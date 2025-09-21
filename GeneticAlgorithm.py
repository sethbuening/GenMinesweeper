from deap import base
from deap import creator
from deap import tools
import copy, random, statistics, minesweeper1, math, time

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

random.seed(0)

WIDTH = 12
HEIGHT = 12
BOMBS = 15

# Initialize AI constants
NEURONS = [WIDTH*HEIGHT, math.floor(WIDTH*HEIGHT/4), math.floor(WIDTH*HEIGHT/16), math.floor(WIDTH*HEIGHT/4), WIDTH*HEIGHT] # Manually set NEURONS to be the number of neurons in each layer of a single network
WEIGHTS = 0
BIASES = 0

for i in range(len(NEURONS)-1):
    WEIGHTS += NEURONS[i]*NEURONS[i+1]
for i in range(1, len(NEURONS)):
    BIASES += NEURONS[i]
PARAMETERS = WEIGHTS+BIASES
INITIAL_RANGE = 0.5

# Constants for the evaluation loop
POPULATION_SIZE = 20000
LOADING_SIZE = 50

# Selection constants
ELITEP = .05 #.02 # Fraction of top individuals that will proceed no matter what
TS = 125 #3 # Tournament size
NOT = int(POPULATION_SIZE * (1-ELITEP)) # to keep the population size the same over time

# Probabilites for crossover and mutation
CXPB = 0.70 # 0.75
MUTPB = 0.175 # 0.2

avgRuntime = 0.01 # the average time it takes for a simulation to run, in seconds. Only used for loading. 7/5 is average for one simulation run without repeat.

def evaluate_individual(individual):
    weights = [individual[i] for i in range(WEIGHTS)]
    biases = [individual[i] for i in range(WEIGHTS, PARAMETERS)]
    return minesweeper1.run(WIDTH, HEIGHT, BOMBS, weights, biases, neurons=NEURONS, test=False) # minesweeper run function returns the score

# Multiple of the same individual may end up selected, but this is ok because they will all crossover and mutate
def select_individuals(population):
    selected = []
    # Elitism
    selected.extend([toolbox.clone(ind) for ind in tools.selBest(population, int(len(population)*ELITEP))])
    # Tournament Selection
    selected.extend([toolbox.clone(ind) for ind in tools.selTournament(population, NOT, TS)])
    return selected

toolbox = base.Toolbox()

# Function for creating random numbers for the initial weights and biases
toolbox.register("randomNum", random.uniform, -INITIAL_RANGE, INITIAL_RANGE)
# Creates individual() which initializes an individual with n random float values inside of its list
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.randomNum, n=PARAMETERS)
# Creates a function to clone individuals; this is supposed to be the default argument but here it is just in case
toolbox.register("clone", copy.deepcopy)

# Creates the 4 core genetic algorithm functions and allows access to them from the toolbox
toolbox.register("evaluate", evaluate_individual)
toolbox.register("select", select_individuals)
toolbox.register("mate", tools.cxTwoPoint) # Previously cxUniform, indpb=0.5. indpb = Probability for the genes to switch
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.15, indpb=0.05) # mean = 0, stdev = 0.15, 
                                                                            # chance for each value (not individual) to mutate = 0.05
# function to initialize population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Initialize and evaluate the first population
population = toolbox.population(n=POPULATION_SIZE)

for ind in population:
    ind.fitness.values = (evaluate_individual(ind),)

    # Create loading variables
    i = population.index(ind)+1
    x = int((i/POPULATION_SIZE)*LOADING_SIZE)
    timeLeft = avgRuntime*(POPULATION_SIZE-i)
    # Loading is only updated once per simulation run
    print(" "*(LOADING_SIZE+50), end="\r") # clear the line to print again
    print(
        f"Gen1:{str(len(population))}Loading|" + "#"*x + "-"*(LOADING_SIZE-x) + 
        f"| eta: {str(int(timeLeft/60))} minutes, {str(int(timeLeft%60))} seconds", 
        end="\r"
        )
print(f"Gen1:{str(len(population))}Evaluated" + " "*(35+LOADING_SIZE))
# Determine the highest fitness value, initialize hall of fame
fitnesses = [ind.fitness.values[0] for ind in population]
stdev = statistics.stdev(fitnesses)
bestFitness = max(fitnesses)
print(f"Gen1:BestFitness: {str(bestFitness)} | stdev: {str(stdev)}")
hallOfFame = [toolbox.clone(tools.selBest(population, 1)[0])]





# Begin the loop (selection, crossover, mutation, evaluate fitness)
# Loop runs until a specified fitness goal is reached
fitnessGoal = WIDTH*HEIGHT - BOMBS # 114
generationNum = 2 # First generation has already run
while (bestFitness < fitnessGoal): #bestFitness < fitnessGoal
    # Selection
    offspring = toolbox.select(population)
    mutCount = 0
    crossCount = 0

    # Crossover
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if(random.random() < CXPB):
            if((child1.fitness.values != (bestFitness,) and child2.fitness.values != (bestFitness,)) or crossCount > 0):
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
            else:
                crossCount = crossCount + 1
            
    # Mutation
    for individual in offspring:
        if(random.random() < MUTPB):
            if(individual.fitness.values != (bestFitness,) or mutCount > 0):
                toolbox.mutate(individual)
                del individual.fitness.values
            else:
                mutCount = mutCount + 1
            #individual = [max(0.001, value) for value in individual] # Ensures that values are never negative and neurons never deactivate

    # Evaluate fitness if the individual does not already have a fitness
    invalid_individuals = [ind for ind in offspring if not ind.fitness.valid]
    for i in range(len(invalid_individuals)):
        invalid_individuals[i].fitness.values = (evaluate_individual(invalid_individuals[i]),)
        x = int(((i+1)/(len(invalid_individuals)))*LOADING_SIZE)
        timeLeft = avgRuntime*(len(invalid_individuals)-(i+1))
        print(" "*(LOADING_SIZE+50), end="\r") # clear the line to print again
        print(
            f"Gen{str(generationNum)}:{str(len(invalid_individuals))}Loading|" + "#"*x + "-"*(LOADING_SIZE-x) + 
            f"| eta: {str(int(timeLeft/60))} minutes, {str(int(timeLeft%60))} seconds", 
            end="\r"
            )
    print(f"Gen{str(generationNum)}:{str(len(invalid_individuals))}Evaluated" + " "*(35+LOADING_SIZE))
    
    # Update fitnesses
    fitnesses = [ind.fitness.values[0] for ind in offspring]

    # Print off statistics
    stdev = statistics.stdev(fitnesses)
    bestFitness = max(fitnesses)
    print("Gen" + str(generationNum) + ":BestFitness: " + str(bestFitness) + " | stdev: " + str(stdev))

    # The offspring entirely replaces the population
    population = offspring[:]
    hallOfFame.append(toolbox.clone(tools.selBest(population, 1)[0]))
    generationNum += 1
#print(hallOfFame[-1])
print("Ran all of the code")
# TODO: Write the entire hall of fame into a separate file as it processes