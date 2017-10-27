import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import random
import math
import time
import sys

# if all u[i] <= v[i] and atleast 1 u[i] < v[i]
def paretoDominant(u, v):
    strict = 0
    for i, j in zip(u, v):
        if i > j:
            return False
        if i < j:
            strict = 1
    return strict == 1

# draw vector u and v with matplotlib and save as image
def exportPlot(u, v, ofile):
    plt.scatter(u, v) # plot points
    # plt.plot(x, y, color='r', lw='2') # plot pareto set
    plt.savefig(ofile) # export plot

######################## MAIN ###########################
u = random.sample(range(100), 30)
v = random.sample(range(100), 30)
exportPlot(u, v, 'output.png')
print paretoDominant(u, v)
