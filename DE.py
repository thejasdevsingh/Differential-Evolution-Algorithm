
import random

# COST FUNCTIONS

def func1(x):
    # Sphere function, bounds = [(-1,1),(-1,1)], f(0,...,0)=0
    return sum([x[i]**2 for i in range(len(x))])

def func2(x):
    # Beale's function, bounds=[(-4.5, 4.5),(-4.5, 4.5)], f(3,0.5)=0.
    term1 = (1.500 - x[0] + x[0]*x[1])**2
    term2 = (2.250 - x[0] + x[0]*x[1]**2)**2
    term3 = (2.625 - x[0] + x[0]*x[1]**3)**2
    return term1 + term2 + term3
	


def func3(x):
	a1 = x[0]**2
	a2 = x[1]**2
	a3 = x[2]**2
	return a1 + a2 + a3
	
	
# CONSTANTS

cost_function = func3					# Cost function
bounds = [(-1,1),(-1,1), (-1,1)]				# Bounds [(x1_min, x1_max), (x2_min, x2_max),...]
population_size = 10					# Population size, must be >= 4
F = 2									# Mutation factor [0,2]
CR = 0.7								# Recombination rate [0,1]
max_generation = 200					# Max number of generations (max_generation)
	
	

# METHODS


def process_bounds(vec, bounds):

    vec_new = []
    # cycle through each element in vector 
    for i in range(len(vec)):

        # variable exceedes the lower bound
        if vec[i] < bounds[i][0]:
            vec_new.append(bounds[i][0])

        # variable exceedes the upper bound
        if vec[i] > bounds[i][1]:
            vec_new.append(bounds[i][1])

        # the variable lies between the range
        if bounds[i][0] <= vec[i] <= bounds[i][1]:
            vec_new.append(vec[i])
        
    return vec_new


# MAIN

def main(cost_function, bounds, population_size, F, CR, max_generation):

    # INITIALIZE A POPULATION
    
    population = []
    for i in range(0,population_size):
        indv = []
        for j in range(len(bounds)):
            indv.append(random.uniform(bounds[j][0],bounds[j][1]))
        population.append(indv)

    # cycle through each generation
    for i in range(1,max_generation+1):
        print 'GENERATION:',i

        gen_scores = [] # score keeping

        # cycle through each individual in the population
        for j in range(0, population_size):

            # MUTATION
            
            # select three random vector index positions [0, population_size), not including current vector (j)
            canidates = range(0,population_size)
            canidates.remove(j)
            random_index = random.sample(canidates, 3)

            x_1 = population[random_index[0]]
            x_2 = population[random_index[1]]
            x_3 = population[random_index[2]]
            x_t = population[j]     # target individual

            # subtract x3 from x2, and create a new vector (x_diff)
            x_diff = [x_2_i - x_3_i for x_2_i, x_3_i in zip(x_2, x_3)]

            # multiply x_diff by the mutation factor (F) and add to x_1
            mutant_vector = [x_1_i + F * x_diff_i for x_1_i, x_diff_i in zip(x_1, x_diff)]
            mutant_vector = process_bounds(mutant_vector, bounds)

            # CROSSOVER

            v_trial = []
            for k in range(len(x_t)):
                crossover = random.random()
                if crossover <= CR:
                    v_trial.append(mutant_vector[k])

                else:
                    v_trial.append(x_t[k])
                    
            # SELECTION
			
            score_trial  = cost_function(v_trial)
            score_target = cost_function(x_t)

            if score_trial < score_target:
                population[j] = v_trial
                gen_scores.append(score_trial)
                print '   >',score_trial, v_trial

            else:
                print '   >',score_target, x_t
                gen_scores.append(score_target)

        # RESULTS
        gen_avg = sum(gen_scores) / population_size					# current generation avg. fitness
        gen_best = min(gen_scores)									# fitness of best individual
        gen_sol = population[gen_scores.index(min(gen_scores))]		# solution of best individual

        print '      > GENERATION BEST:',gen_best
        print '      > BEST SOLUTION:',gen_sol,'\n'

    return gen_sol


# RUN

main(cost_function, bounds, population_size, F, CR, max_generation)
