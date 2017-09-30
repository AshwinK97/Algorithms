import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import math
import time
import sys

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

# check where line intersects with polygon and extend it
def extendLine(vList, v1, v2):
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

        # check if intersection was on endpoint
        # check if intersection is within bounds v1, v2
        if (poi_x <= v1[0] and poi_x >= v2[0]) or (poi_x <= v2[0] and poi_x >= v1[0]):
            # if intersection is on the endpoint v3
            if [poi_x, poi_y] == v3:
                # intersects between line v1, v2
                if (v3[0] > v1[0] and v3[0] < v2[0]) or (v3[0] < v1[0] and v3[0] > v2[0]):
                    break
                else:
                    continue
            # if intersection is on the endpoint v4
            if [poi_x, poi_y] == v4:
                # intersects between line v1, v2
                if (v4[0] > v1[0] and v4[0] < v2[0]) or (v4[0] < v1[0] and v4[0] > v2[0]):
                    break
                else:
                    continue
            # if intersection is not on an endpoint, break
            else:
                # v1, v2 = [0, 0], [0, 0] # comment this out for test case 1
                break

        # if intersection was outside of v1, v2 but inside of v3, v4
        elif (poi_x <= v3[0] and poi_x >= v4[0]) or (poi_x <= v4[0] and poi_x >= v3[0]):
            if (poi_y <= v3[1] and poi_y >= v4[1]) or (poi_y <= v4[1] and poi_y >= v3[1]):
                # v1 is right, v2 is left
                if (v1[0] > v2[0]):
                    if poi_x > v1[0]:
                        v1 = [poi_x, poi_y]
                    else:
                        v2 = [poi_x, poi_y]
                # v2 is right, v1 is left
                elif (v1[0] < v2[0]):
                    if poi_x > v1[0]:
                        v2 = [poi_x, poi_y]
                    else:
                        v1 = [poi_x, poi_y]
                # v1 is above, v2 is below
                elif (v1[1] > v2[1]):
                    if poi_y > v1[1]:
                        v1 = [poi_x, poi_y]
                    else:
                        v2 = [poi_x, poi_y]
                # v2 is above, v1 is below
                elif (v1[1] < v2[1]):
                    if poi_y > v1[1]:
                        v2 = [poi_x, poi_y]
                    else:
                        v1 = [poi_x, poi_y]

                # recursive call extendline
                t1, t2 = extendLine(vList, v1, v2)
                if t1 == [0, 0] and t2 == [0, 0]:
                    break
                v1, v2 = t1, t2

        # ignore intersection if it occurs outside of the polygon
        else:
            continue

    return v1, v2

# return the x1, x2 and y1, y2 for the maximum line
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
            tmax = getDistance(tv1, tv2)
            # check if new line is longer than old max line
            if tmax > max:
                mx[0] = tv1[0]
                mx[1] = tv2[0]
                my[0] = tv1[1]
                my[1] = tv2[1]
                max = tmax

    # print the points and the length of max line
    print "A(" + str(mx[0]) + ", " + str(my[0])+ ")"
    print "B(" + str(mx[1]) + ", " + str(my[1])+ ")"
    print "max landing strip = " + str(max)
    return mx, my

# draw the polygon and line and save as image
def exportPlot(vList, mx, my, ofile):
    plt.fill(*zip(*vList), fill=False, color='green', lw='2')
    plt.plot(mx, my, color='r', lw='2') # plot([x1, x2], [y1, y2])
    plt.savefig(ofile)

# read the input file, return list of vertices
def getInput(inFile):
    vList = []
    with open(inFile) as f:
        f.readline().strip() # dump # of lines
        for v in f:
            vList.append(map(float, v.split())) # read as float arrays
    return vList

##################### MAIN #####################
vList = getInput(sys.argv[1]) # get list of vertices
start = time.time() # get starting time
mx, my = maxLine(vList) # max line aglorithm
print "runtime for '" + str(sys.argv[1]) + "': " + str(round(time.time() - start, 6)) + " seconds" # calculate and display runtime
exportPlot(vList, mx, my, 'output.png') # draw plot and save
