import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# Function implementations
hce = lambda x: sum([np.power(1000000.0, (i)/(len(x)-1)) * (xC ** 2) for i, xC in enumerate(x)])

bent_cigar = lambda x: x[0]**2 + (10**6)*sum(np.power(x[1:], 2))

discus = lambda x: (10**6)*(x[0]**2) + sum(np.power(x[1:], 2))

rosenbrock = lambda x: sum(100 * np.power((np.power(x[:-1], 2) \
	- x[1:]), 2) + np.power((x[:-1] - 1), 2))

ackley = lambda x: -20 * np.exp(-0.2 * np.sqrt(sum(np.power(x, 2))/len(x))) - \
	np.exp(sum(np.cos(2*np.pi*x))/len(x)) + 20 + np.exp(1)

weierstrass = lambda x: sum(sum(map(lambda k: np.power(0.5, k) * \
	np.cos(2*np.pi*np.power(3, k) * (np.array(x) + 0.5)) , range(1, 21)))) \
	 - len(x) * (sum(map(lambda k: np.power(0.5, k) * np.cos(2*np.pi * \
	np.power(3, k) * 0.5) , range(1, 21))))

griewank = lambda x: sum(np.power(x, 2)/4000) - \
	np.prod([np.cos(a/ (i + 1)) + 1 for i, a in enumerate(x)])

rastrigrin = lambda x: sum(np.power(x, 2) - 10*np.cos(2*np.pi*x) + 10)

katsuura = lambda x: (10/len(x)) * np.prod(np.power(([1+ i * \
	sum(map(lambda j: abs(np.power(2, j) * item - \
	np.round(np.power(2, j) * item)) / np.power(2, j), \
	range(1, 33))) for i, item in enumerate(x)]), (10 \
	/ np.power(len(x), 1.2)))) - (10 / np.power(len(x), 2))

# plot the specified function in 3 dimensions
def plot3D(fun, fname):
	fig = plt.figure(figsize=(10, 8))
	ax = fig.add_subplot(111, projection='3d')
	x = np.linspace(-10, 10, 100)
	y = np.linspace(-10, 10, 100)
	X, Y = np.meshgrid(x, y)
	Z = fun(np.asarray([X, Y]))
	ax.plot_surface(X, Y, Z, cmap=cm.winter)
	ax.set_xlabel('X axis')
	ax.set_ylabel('Y axis')
	ax.set_zlabel('Z axis')
	plt.savefig(fname)

# differential evolution algorithm
def de(fun, bounds, mut=0.8, crossp=0.9, popsize=100, its=3000):
	dimensions = len(bounds)
	pop = np.random.rand(popsize, dimensions)
	min_b, max_b = np.asarray(bounds).T
	diff = np.fabs(min_b - max_b)
	pop_denorm = min_b + pop * diff
	fitness = np.asarray([fun(ind) for ind in pop_denorm])
	best_idx = np.argmin(fitness)
	best = pop_denorm[best_idx]
	for i in range(its):
		for j in range(popsize):
			idxs = [idx for idx in range(popsize) if idx != j]
			a, b, c = pop[np.random.choice(idxs, 3, replace = False)]
			mutant = np.clip(a + mut * (b - c), 0, 1)
			cross_points = np.random.rand(dimensions) < crossp
			if not np.any(cross_points):
				cross_points[np.random.randint(0, dimensions)] = True
			trial = np.where(cross_points, mutant, pop[j])
			trial_denorm = min_b + trial * diff
			f = fun(trial_denorm)
			if f < fitness[j]:
				fitness[j] = f
				pop[j] = trial
				if f < fitness[best_idx]:
					best_idx = j
					best = trial_denorm
		yield best, fitness[best_idx]

# particle swarm algorithm
def pso(fun, dimensions, min = -10, max = 10, its = 3000, populationSize = 100, c1 = 2.05, c2 = 2.05, w = 0.65, wdamp = 0.995):

	# Empty Particle Template
	empty_particle = {
		'position': None,
		'velocity': None,
		'cost': None,
		'best_position': None,
		'best_cost': None,
	};

	# Extract Problem Info
	CostFunction = fun;
	min = -10;
	max = 10;

	# Initialize Global Best
	gbest = {'position': None, 'cost': np.inf};

	# Create Initial population
	population = [];
	for i in range(0, populationSize):
		population.append(empty_particle.copy());
		population[i]['position'] = np.random.uniform(min, max, dimensions);
		population[i]['velocity'] = np.zeros(dimensions);
		population[i]['cost'] = CostFunction(population[i]['position']);
		population[i]['best_position'] = population[i]['position'].copy();
		population[i]['best_cost'] = population[i]['cost'];
		
		if population[i]['best_cost'] < gbest['cost']:
			gbest['position'] = population[i]['best_position'].copy();
			gbest['cost'] = population[i]['best_cost'];
	
	# PSO Loop
	for it in range(0, its):
		for i in range(0, populationSize):
			
			population[i]['velocity'] = w*population[i]['velocity'] \
				+ c1*np.random.rand(dimensions)*(population[i]['best_position'] - population[i]['position']) \
				+ c2*np.random.rand(dimensions)*(gbest['position'] - population[i]['position']);

			population[i]['position'] += population[i]['velocity'];
			population[i]['position'] = np.maximum(population[i]['position'], min);
			population[i]['position'] = np.minimum(population[i]['position'], max);

			population[i]['cost'] = CostFunction(population[i]['position']);
			
			if population[i]['cost'] < population[i]['best_cost']:
				population[i]['best_position'] = population[i]['position'].copy();
				population[i]['best_cost'] = population[i]['cost'];

				if population[i]['best_cost'] < gbest['cost']:
					gbest['position'] = population[i]['best_position'].copy();
					gbest['cost'] = population[i]['best_cost'];

		w *= wdamp;
		# print('Iteration {}: Best Cost = {}'.format(it, gbest['cost']));

		yield gbest['cost'];


#-- get 3D surface plot of each function --*
# plot3D(hce, './plots/High Conditioned Elliptic Function.png')
# plot3D(bent_cigar, './plots/Bent Cigar Function.png')
# plot3D(discus, './plots/Discus Function.png')
# plot3D(rosenbrock, './plots/Rosenbrock\'s Function')
# plot3D(ackley, './plots/Ackley\'s Function')
# plot3D(weierstrass, './plots/Weierstrass Function')
# plot3D(rastrigrin, './plots/Rastrigrin\'s Function')
# plot3D(griewank, './plots/Griewank\'s Function')
# plot3D(katsuura, './plots/Katsuura Function')

# run DE and PSO on different benchmark functions, for required dimensions
for d in [2, 5, 10]:
	# get stats for DE
	outputDE = list(de(griewank, bounds=[(-10, 10)] * d))
	x, f = zip(*outputDE)
	plt.plot(f)
	plt.show()
	plt.clf()

	# get stats for PSO
	outputPSO = list(pso(griewank, its = 200, populationSize = 100, c1 = 2.05, c2 = 2.05, w = 0.65, wdamp = 0.995, dimensions=d))
	plt.plot(outputPSO)
	plt.show()



# for d in range (0, 51):

# outputPSO = list(pso(hce, its = 200, populationSize = 100, c1 = 2.05, c2 = 2.05, w = 0.65, wdamp = 0.995, dimensions=2))
# plt.plot(outputPSO, label='red=PSO')
# plt.legend()

# print list(pso(ackley, its = 200, populationSize = 100, c1 = 2.05, c2 = 2.05, w = 0.65, wdamp = 0.995, dimensions=2))

# plt.plot(outputPSO)
# plt.show()


