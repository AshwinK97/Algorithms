import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import math
import time

# returns the intersecction of two lines
def getIntersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return "parallel", 0 # no intersection

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

# return the distance between 2 vertices rounded to 6 decimals and the two new vertice
def getDistance(v1, v2):
    return round(math.sqrt((float(v2[0])-float(v1[0]))**2 + (float(v2[1])-float(v1[1]))**2), 6)

# replaces either v1 or v2 with (poi_x, poi_y) ############################# FIX THIS
def replacePoint(v1, v2, poi_x, poi_y):
    if v1[0] > v2[0]:
    	if poi_x > v1[0]:
    		v1[0] = poi_x
    		v1[1] = poi_y
    	elif poi_x < v2[0]:
    		v2[0] = poi_x
    		v2[1] = poi_y
    	else:
    		return [0, 0], [0, 0], 0
    else:
    	if poi_x > v2[0]:
    		v2[0] = poi_x
    		v2[1] = poi_y
    	elif poi_x < v1[0]:
    		v1[0] = poi_x
    		v1[1] = poi_y
    	else:
    		return [0, 0], [0, 0], 0

    return v1, v2, 1

# check where line intersects with polygon and extend it
def extendLine(vList, v1, v2):
    iCount = 0 # number of intersections
    for i, v3 in enumerate(vList):

        # get v4 for the other line
    	if (i==len(vList)-1):
            v4 = vList[0]
        else:
            v4 = vList[i+1]

        # get the point of intersection
        poi_x, poi_y = getIntersection([v1, v2], [v3, v4])

        # if the lines are parallel, skip
        if poi_x == "parallel":
            continue

        # check if intersection is within bounds v1, v2
        if (poi_x <= v1[0] and poi_x >= v2[0]) or (poi_x <= v2[0] and poi_x >= v1[0]):
            if [poi_x, poi_y] == v3 or [poi_x, poi_y] == v4:
                continue
            else:
                break

        # if intersection was outside of v1, v2
            # use replace point to change either v1 or v2
                #

        # v1, v2, c = replacePoint(v1, v2, poi_x, poi_y)
    return v1, v2

# return the maximum line
def maxLine(vList):
    mx = [0, 0] # x1, x2 for max line
    my = [0, 0] # y1, y2 for max line
    max = 0 # distance of max line

    # loop through all combinations of points
    for i, v1 in enumerate(vList):
        for j, v2 in enumerate(vList):

            # dont make line out of the same point
            if j == i:
                continue

            # try to extend this line
            tv1, tv2 = extendLine(vList, v1, v2)

            # get the distance between the two points
            tmax = getDistance(v1, v2)

            # check if new line is longer than old max line
            if tmax > max:
                mx[0] = tv1[0]
                mx[1] = tv2[0]
                my[0] = tv1[1]
                my[1] = tv2[1]
                max = tmax

    # print the points and the length of max line
    print "x1="+str(mx[0])  + ", " + "x2="+str(mx[1])
    print "y1="+str(my[0]) + ", " + "y2="+str(my[1])
    print "max landing strip = " + str(max)
    return mx, my

# save output as a png
def exportPlot(vList, mx, my):
    plt.fill(*zip(*vList), fill=False, color='green', lw='2')
    plt.plot(mx, my, color='r', lw='2') # plot([x1, x2], [y1, y2])
    plt.savefig('output.png')

# read the input file, return list of vertices
def getInput(inFile):
    vList = []
    with open(inFile) as f:
        f.readline().strip() # read the number of lines
        for v in f:
            vList.append(map(float, v.split()))
    return vList

##################### MAIN #####################
vList = getInput('input.txt') # get list of vertices
start = time.time() # get starting time
mx, my = maxLine(vList) # get max line
print "runtime " + str(time.time() - start) + " seconds" # calculate and display runtime
exportPlot(vList, mx, my) # draw plot and save
