import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import math
import time

def replacePoint(vList, v1, v2, poi_x, poi_y):
    # replace v1 v2 for normal line
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

    # print v1, v2
    return v1, v2, 1

# check where line intersects with polygon and return new bounds
def checkIntersection(vList, lcList, v1, v2):

    m, b = getLinear(v1, v2)
    count = 0

    for i, l in enumerate(lcList):

    	if count >= 1:
        	break

    	# get the other line's vertices
    	lv1 = vList[i]
    	if (i==len(vList)-1):
            lv2 = vList[0]
        else:
            lv2 = vList[i+1]

        ################# Parallel Lines ####################
        if m == l[0]:
            continue

        ################# Vertical Lines ####################
        elif m == 'infinite': # if given line is vertical
        	# m is 'infinite'
        	# b is the x-intercept
        	poi_y = l[0] * b + l[1]  # intersection y-val
        	poi_x = b                # intersection x-val

        elif l[0] == 'infinite': # if line in list is vertical
        	# l[0] is 'infinite'
        	# l[1] is x intercept
        	poi_y = m * l[1] + b # intersection y-val
        	poi_x = l[1]         # intersection x-val

        ################# Horizontal Lines ##################
        elif m == 0:
        	poi_x = (b - l[1]) / l[0]
        	poi_y = l[0] * poi_x + l[1]

        elif l[0] == 0:
        	poi_x = (l[1] - b) / m
        	poi_y = m * poi_x + b

        ################# 2 Diagonal Lines ##################
        else:
            poi_x = (l[1] - b) / (l[0] - b)
            poi_y = m * poi_x + b

        # check if intersection occured at an end point
        if [poi_x, poi_y] == [float(lv1[0]), float(lv1[1])] or [poi_x, poi_y] == [float(lv2[0]), float(lv2[1])]: # intersection at endpoint
        	continue

        # check if point of intersection is within v1, v2 and lv1, lv2
        if poi_x <= v1[0] and poi_x :
            v1, v2, c = replacePoint(vList, v1, v2, poi_x, poi_y)
        count += c

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
            tmax, tv1, tv2 = getDistance(vList, lcList, v1, v2)
            if tmax > max:
                mx[0] = tv1[0]
                mx[1] = tv2[0]
                my[0] = tv1[1]
                my[1] = tv2[1]
                max = tmax

    print "x1="+str(mx[0])  + ", " + "x2="+str(mx[1])
    print "y1="+str(my[0]) + ", " + "y2="+str(my[1])
    print "max landing strip = " + str(max)
    return mx, my

# save output as a png
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

    for i, v1 in enumerate (vList): # get m and b value for each line
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
mx, my = maxLine(vList, lcList) # get max line
exportPlot(vList, mx, my) # draw plot and save
print "runtime " + str(time.time() - start) + " seconds" # calculate and display runtime
