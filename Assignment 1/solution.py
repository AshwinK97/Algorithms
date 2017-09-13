import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import math

# check if proposed line intersects with polygon
def checkIntersection(v1, v2):
    pass    

def getDistance(v1, v2):
    return round(math.sqrt((int(v2[0])-int(v1[0]))**2 + (int(v2[1])-int(v1[1]))**2), 6)

# works for convex polygons
def maxLine(vCount, vList):
    mx = [0, 0] # x1, x2 for max line
    my = [0, 0] # y1, y2 for max line
    max = 0 # distance of max line

    for i, v1 in enumerate(vList):
        for j, v2 in enumerate(vList):
            if j == i: # dont check the same point
                continue
            tmax = getDistance(v1, v2)
            if (tmax > max):
                mx[0] = v1[0]
                mx[1] = v2[0]
                my[0] = v1[1]
                my[1] = v2[1]
                max = tmax
    print "x1="+str(mx[0])  + ", " + "x2="+str(mx[1])
    print "y1="+str(my[0]) + ", " + "y2="+str(my[1])
    print "max landing strip = " + str(max)
    return mx, my

# save output as a jpeg
def exportPlot(vList, mx, my):
    # plt.axis('off')
    plt.fill(*zip(*vList), fill=False, color='green', lw='2')
    plt.plot(mx, my, color='r', lw='2') # plot([x1, x2], [y1, y2])
    plt.savefig('output.jpg')


# read the input file, get number of vertices and list of vertices
def getInput(inFile):
    vCount = 0
    vList = []
    with open(inFile) as f:
        vCount = f.readline().strip()
        for v in f:
            vList.append(v.strip().split(' '))
    return vCount, vList


##################### MAIN #####################
inFile = 'input.txt' # name of file with input data
vCount, vList = getInput(inFile) # get list of vertices

mx, my = maxLine(vCount, vList)
exportPlot(vList, mx, my)
