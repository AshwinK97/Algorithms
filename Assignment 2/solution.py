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
def exportPlot(u, v, ofile):
    plt.plot(u, color='r', lw='2')
    plt.plot(v, color='b', lw='2')
    plt.savefig(ofile)

######################## MAIN ###########################
u = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
v = [1, 2, 3, 4, 5, 6, 7, 9, 9, 10]
exportPlot(u, v, 'output.png')
print paretoDominant(u, v)
