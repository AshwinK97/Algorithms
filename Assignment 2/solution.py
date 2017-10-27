import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import random, math, time, sys

# return the pareto front set for the given mode
def paretoDominant(u, v, mode):
    if mode == 0: # low u and low v
        # sort points by y, x, ascending
        points = sorted(zip(u, v), key=lambda k: [k[1], k[0]])
        front = points[0] # starting point will be the left most
        pareto = [front] # store the pareto front set
        # if x is greater than or equal, add to front
        for p in points:
            if p[0] >= front[0]:
                front = p
                pareto.append(front)
    elif mode == 1: # low u and high v
        # sort points by y, x, ascending
        points = sorted(zip(u, v), key=lambda k: [k[1], k[0]])
        front = points[0] # starting point will be the left most
        pareto = [front] # store the pareto front set
        # if x is less than or equal, add to front
        for p in points:
            if p[0] <= front[0]:
                front = p
                pareto.append(front)
    elif mode == 2: # high u and low v
        # sort points by x, y, ascending
        points = sorted(zip(u, v), key=lambda k: [k[0], k[1]])
        front = points[0] # starting point will be the left most
        pareto = [front] # store the pareto front set
        # if y is greater than or equal to, add to front
        for p in points:
            if p[1] >= front[1]:
                front = p
                pareto.append(front)
    elif mode == 3: # high u and high v
        # sort points by x, y, descending
        points = sorted(zip(u, v), key=lambda k: [k[0], k[1]], reverse=True)
        front = points[0] # starting point will be the left most
        pareto = [front] # store the pareto front set
        # if y is greater than or equal to, add to front
        for p in points:
            if p[1] >= front[1]:
                front = p
                pareto.append(front)

    return pareto
    

# draw vector u and v with matplotlib and save as image
def exportPlot(u, v, pu, pv, ofile):
    plt.scatter(u, v)                   # plot points
    plt.plot(pu, pv, color='r', lw='1') # plot pareto set
    plt.savefig(ofile)                  # export plot
    plt.clf()

######################## MAIN ###########################
u, v = [random.sample(range(100), 20), random.sample(range(100), 20)] # random vectors
for case in range(0, 4):
    pareto = paretoDominant(u, v, case)
    pu = [i[0] for i in pareto] # get x-vals for pareto front set
    pv = [i[1] for i in pareto] # get y-vals for pareto front set
    exportPlot(u, v, pu, pv, 'output' + str(case+1) + '.png')
