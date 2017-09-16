import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import math

# check if proposed line intersects with polygon
def checkIntersection(vList, lList, v1, v2):
    # get linear componetns of the line (v1, v2)
    # check 
    pass    

# return the distance between 2 vertices rounded to 6 decimals
def getDistance(v1, v2):
    return round(math.sqrt((float(v2[0])-float(v1[0]))**2 + (float(v2[1])-float(v1[1]))**2), 6)

# return slope and y-intercept for given 2 vertices
# if given vertices create a vertical line, return 'infinite' as slope and x-intercept as b
def getLinear(v1, v2):
    if float(v2[0]) - float(v1[0]) == 0: # check for vertical line
        m = 'infinite'
        b = float(v1[0]) # treat this as x-intercept
    else:
        m = (float(v2[1]) - float(v1[1])) / (float(v2[0]) - float(v1[0])) # y2-y1/x2-x1
        b = float(v1[1]) - float(m)*float(v1[0])                    # y - mx
    return m, b

def maxLine2(vList, lList):
    pass

# works for convex polygons
def maxLine(vList):
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
    plt.savefig('output.png')


# read the input file, return list of vertices and list of lines
def getInput(inFile):
    vList = []
    lList = []
    with open(inFile) as f:
        f.readline().strip()
        for v in f:
            vList.append(v.strip().split(' '))

    for i, v1 in enumerate (vList):
        if (i==len(vList)-1):
            v2 = vList[0]
        else:
            v2 = vList[i+1]
        lList.append(getLinear(v1, v2))

    return vList, lList


##################### MAIN #####################
inFile = 'input.txt' # name of file with input data
vList, lList = getInput(inFile) # get list of vertices
print vList
print lList

# mx, my = maxLine(vList)
mx, my = maxLine2(vList, lineList)
# exportPlot(vList, mx, my)
