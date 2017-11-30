import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function implementations
hce = lambda x: sum([np.power(1000000.0, (i)/(d-1)) * (xC ** 2) for i, xC in enumerate(x)])

bent_cigar = lambda x: x[0]**2 + (10**6)*sum(np.power(x[1:], 2))

discus = lambda x: (10**6)*(x[0]**2) + sum(np.power(x[1:], 2))

rosenbrock = lambda x: sum(100 * np.power((np.power(x[:-1], 2) \
	- x[1:]), 2) + np.power((x[:-1] - 1), 2))

def ackley(x):
	return -20 * np.exp(-0.2 * np.sqrt(sum(np.power(x, 2))/len(x))) - np.exp(sum(np.cos(2*np.pi*x))/len(x)) + 20 + np.exp(1)

ackley = lambda x: -20 * np.exp(-0.2 * np.sqrt(sum(np.power(x, 2))/len(x))) - \
	np.exp(sum(np.cos(2*np.pi*x))/len(x)) + 20 + np.exp(1)

weierstrass = lambda x: sum(sum(map(lambda k: np.power(0.5, k) * \
	np.cos(2*np.pi*np.power(3, k) * (np.array(x) + 0.5)) , range(1, 21)))) \
	 - len(x) * (sum(map(lambda k: np.power(0.5, k) * np.cos(2*np.pi * \
	np.power(3, k) * 0.5) , range(1, 21))))

griewank = lambda x: sum(np.power(x, 2)/4000) - \
	np.prod([np.cos(item / (i + 1)) + 1 for i, a in enumerate(x)])

rastrigrin = lambda x: sum(np.power(x, 2) - 10*np.cos(2*np.pi*x) + 10)

katsuura = lambda x: (10/len(x)) * np.prod(np.power(([1+ i * \
	sum(map(lambda j: abs(np.power(2, j) * item - \
	np.round(np.power(2, j) * item)) / np.power(2, j), \
	range(1, 33))) for i, item in enumerate(x)]), (10 \
	/ np.power(len(x), 1.2)))) - (10 / np.power(len(x), 2))

def plot3d(fun):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	x = np.linspace(-10, 10, 100)
	y = np.linspace(-10, 10, 100)
	X, Y = np.meshgrid(x, y)
	Z = fun(np.asarray([X, Y]))

	ax.plot_surface(X, Y, Z)

	ax.set_xlabel('X axis')
	ax.set_ylabel('Y axis')
	ax.set_zlabel('Z axis')

	plt.show()

def de(fobj, bounds, mut=0.8, crossp=0.9, population=100, its=3000):
	dimensions = len(bounds)
	pop = np.random.rand(population, dimensions)
	min_b, max_b = np.asarray(bounds).T
	diff = np.fabs(min_b - max_b)
	pop_denorm = min_b + pop * diff
	fitness = np.asarray([fobj(ind) for ind in pop_denorm])
	best_idx = np.argmin(fitness)
	best = pop_denorm[best_idx]
	for i in range(its):
		for j in range(population):
			idxs = [idx for idx in range(population) if idx != j]
			a, b, c = pop[np.random.choice(idxs, 3, replace = False)]
			mutant = np.clip(a + mut * (b - c), 0, 1)
			cross_points = np.random.rand(dimensions) < crossp
			if not np.any(cross_points):
				cross_points[np.random.randint(0, dimensions)] = True
			trial = np.where(cross_points, mutant, pop[j])
			trial_denorm = min_b + trial * diff
			f = fobj(trial_denorm)
			if f < fitness[j]:
				fitness[j] = f
				pop[j] = trial
				if f < fitness[best_idx]:
					best_idx = j
					best = trial_denorm
		yield best, fitness[best_idx]


# for d in [2, 5, 10]:
# 	output = list(de(ackley, bounds=[(-10, 10)] * d))
# 	print(output[-1])
# 	x, f = zip(*output)
# 	plt.plot(f, label='d={}'.format(d))
# 	plt.legend()
# 	plt.show()
# 	plt.savefig('ackley.png')

plot3d(ackley)