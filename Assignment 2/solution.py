import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import math
import time
import sys

def paretoDominant(u, v):
    
    strict = False
    for i, j in zip(u, v):
        if i > j:
            return False
        if i < j:
            strict = True
    return True, Scrict

def exportPlot(u, v, ofile):
    plt.plot(u, color='r', lw='2')
    plt.plot(v, color='b', lw='2')
    plt.savefig(ofile)

u = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
v = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
exportPlot(u, v, 'output.png')
