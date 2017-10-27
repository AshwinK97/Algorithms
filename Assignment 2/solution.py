import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import random, math, time, sys

# return the pareto front set for the given mode
def paretofront(u, v, mode):
    # low u and low v
    if mode == 1:
        # sort points by y, x, ascending
        points = sorted(zip(u, v), key=lambda k: [k[1], k[0]])
        front = points[0] # starting point will be the left most
        pareto = [front] # store the pareto front set
        for p in points:
            if p[0] >= front[0]: # if x is greater than or equal, add to front
                front = p
                pareto.append(front)
    # high u and high v
    elif mode == 2:
        points = sorted(zip(u, v), key=lambda k: [k[0], k[1]], reverse=True) # sort by x, y, desc
        front = points[0] # starting point will be the left most
        pareto = [front] # store the pareto front set
        for p in points:
            if p[1] >= front[1]: # if y is greater than or equal, add to front
                front = p
                pareto.append(front)
    # low u and high v
    elif mode == 3:
        # sort points by y, x, ascending
        points = sorted(zip(u, v), key=lambda k: [k[1], k[0]])
        front = points[0] # starting point will be the left most
        pareto = [front] # store the pareto front set
        for p in points:
            if p[0] <= front[0]: # if x is less than or equal, add to front
                front = p
                pareto.append(front)
    # high u and low v
    elif mode == 4:
        points = sorted(zip(u, v), key=lambda k: [k[0], k[1]]) # sort by x, y, asc
        front = points[0] # starting point will be the left most
        pareto = [front] # store the pareto front set
        for p in points:
            if p[1] >= front[1]: # if y is greater than or equal, add to front
                front = p
                pareto.append(front)

    return pareto
    

# draw vector u and v with matplotlib and save as image
def exportPlot(u, v, pu, pv, ofile):
    plt.title('case ' + ofile[6:7])     # title for graph
    plt.xlabel('u', fontsize=14)        # label for x axis
    plt.ylabel('v', fontsize=14)        # label for y axis
    plt.scatter(u, v)                   # plot points
    plt.plot(pu, pv, color='r', lw='1') # plot pareto set
    plt.savefig(ofile)                  # export plot
    plt.clf()                           # clear the figure

######################## MAIN ###########################
u, v = [random.sample(range(20), 20), random.sample(range(20), 20)] # random vectors
print "points:\n", zip(u, v) # print list of points

# CASE 1 - low values for u and v are desirable
pareto = paretofront(u, v, 1) # get pareto set for points with given mode
print "low u low v:\n", pareto[1:] # print pareto set
exportPlot(u, v, [i[0] for i in pareto], [i[1] for i in pareto], 'output1.png') # plot the points

# CASE 2 - high values for u and v are desirable
pareto = paretofront(u, v, 2) # get pareto set for points with given mode
print "high u high v:\n", pareto[1:] # print pareto set
exportPlot(u, v, [i[0] for i in pareto], [i[1] for i in pareto], 'output2.png') # plot the points

# CASE 3 - low values for u and high values for v are desirable
pareto = paretofront(u, v, 3) # get pareto set for points with given mode
print "low u high v:\n", pareto[1:] # print pareto set
exportPlot(u, v, [i[0] for i in pareto], [i[1] for i in pareto], 'output3.png') # plot the points

# CASE 4 - high values for u and low values for v are desirable
pareto = paretofront(u, v, 4) # get pareto set for points with given mode
print "high u low v:\n", pareto[1:] # print pareto set
exportPlot(u, v, [i[0] for i in pareto], [i[1] for i in pareto], 'output4.png') # plot the points