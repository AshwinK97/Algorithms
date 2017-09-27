import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import math
import time

# check where line intersects with polygon and return new bounds
def checkIntersection(vList, lcList, v1, v2):
    m, b = getLinear(v1, v2)
    intersectons = 0
    for i, l in enumerate(lcList):
        if intersectons > 2: # if the line intersects with more than 2 other lines
            return [0, 0], [0, 0]

        if m == l[0]: # exception for parallel lines
            continue

        if m == 'infinite': # if given line is vertical
        	# m is 'infinite'
        	# b is the x-intercept
        	poi_y = l[0] * b + l[1]  # intersection y-val
        	poi_x = b                # intersection x-val 

        if l[0] == 'infinite': # if line in list is vertical
        	# l[0] is 'infinite'
        	# l[1] is x intercept
        	print "correct case"
        	poi_y = m * l[1] + b # intersection y-val
        	poi_x = l[1]         # intersection x-val
        	break

        else: # for normal lines, POI and check if it is within v1 and v2, if not, replace
            poi_y = (l[1] - b) / (m - l[0])
            poi_x = (poi_y - b) / m

    # replace v1 v2 for vertical line
    	# check if v1 or v2 is top or bottom

    # replace v1 v2 for normal line
    if v1[0] > v2[0]:
    	if poi_x > v1[0]:
    		v1[0] = poi_x
    		v1[1] = poi_y
    else:
    	if poi_x > v2[0]:
    		v2[0] = poi_x
    		v2[1] = poi_y

    return v1, v2

# return the distance between 2 vertices rounded to 6 decimals and the two new vertices
def getDistance(vList, lcList, v1, v2):
    v1, v2 = checkIntersection(vList, lcList, v1, v2)
    return round(math.sqrt((float(v2[0])-float(v1[0]))**2 + (float(v2[1])-float(v1[1]))**2), 6), v1, v2

# return slope and y-intercept for given 2 vertices
# if given vertices create a vertical line, return 'infinite' as slope and x-intercept as b
def getLinear(v1, v2):
    if float(v2[0]) - float(v1[0]) == 0: # check for vertical line
        m = 'infinite'
        b = float(v1[0]) # treat this as x-intercept
    else:
        m = (float(v2[1]) - float(v1[1])) / (float(v2[0]) - float(v1[0])) # y2-y1/x2-x1
        b = float(v1[1]) - float(m)*float(v1[0])                          # y - mx
    return m, b

#---sudo algorithm---#
# longest line will always touch atleast 2 vertices
# create lines using the vList, and get their slope and y-int or the x-int for vertical lines
# check these lines for intersection with other lines
    # if they intersect at an end point, this is ok
    # if they intersect anywhere else:
        # check if there are any lines who's points are beyond the currently intersected line
            # if there is another line, this line is not valid
            # it not, then the line is valid

# return the maximum line
def maxLine(vList, lcList):
    mx = [0, 0] # x1, x2 for max line
    my = [0, 0] # y1, y2 for max line
    max = 0 # distance of max line

    # loop through all possible lines
    for i, v1 in enumerate(vList):
        for j, v2 in enumerate(vList):
            if j == i: # dont check the same point
                continue
            tmax = getDistance(vList, lcList, v1, v2)
            if tmax > max:
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
    plt.fill(*zip(*vList), fill=False, color='green', lw='2')
    plt.plot(mx, my, color='r', lw='2') # plot([x1, x2], [y1, y2])
    plt.savefig('output.png')


# read the input file, return list of vertices and list of lines
def getInput(inFile):
    vList = []
    lcList = []
    with open(inFile) as f:
        f.readline().strip() # read the number of lines
        for v in f:
            vList.append(v.strip().split(' ')) # read vertices

    for i, v1 in enumerate (vList):
        if (i==len(vList)-1):
            v2 = vList[0]
        else:
            v2 = vList[i+1]
        lcList.append(getLinear(v1, v2))

    return vList, lcList


##################### MAIN #####################
start = time.time() # get starting time
inFile = 'input.txt' # name of file with input data
vList, lcList = getInput(inFile) # get list of vertices
# mx, my = maxLine(vList, lcList) # get max line
# exportPlot(vList, mx, my) # draw plot and save


max, v1, v2 = getDistance(vList, lcList, [0, 0], [25, 20])
print "max: " + str(max)
exportPlot(vList, [v1[0], v2[0]], [v1[1], v2[1]])

# print "runtime " + str(time.time() - start) + " seconds" # calculate and display runtime
