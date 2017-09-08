import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def exportPlot(vList):
    plt.plot(*zip(*vList))
    plt.savefig('output.jpg')

def snyders(vList):
    p1 = vList[0] 

def getInput(inFile):
    with open(inFile) as f:
        vCount = f.readline().strip() # get the number of vertices
        for v in f:
            vList.append(v.strip().split(' ')) # get list of vertices
    return vCount, vList

##################### Main #####################
inFile = 'input.txt' # name of file with input data
vCount = 0 # number of vertices
vList = [] # list of vertices

vCount, vList = getInput(inFile) # get # of vertices and list of vertices
print vCount
print vList

exportPlot(vList)
