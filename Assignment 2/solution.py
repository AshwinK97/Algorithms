import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
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
def exportPlot(u, v, p, ofile):
    plt.scatter(u, v, color='blue', lw='1')
    plt.plot(p, color='red', lw='1')
    plt.savefig(ofile)

######################## MAIN ###########################
u = np.array([1, 2, 3, 4, 5]) # set u (x-axis)
v = np.array([2, 4, 6, 8, 10]) # set v (y-axis)
p = np.array([]) # set of non dominated points
exportPlot(u, v, p, 'output.png')
print paretoDominant(u, v)
