# Databricks notebook source
sc = spark.sparkContext
import math
dbutils.fs.mkdirs("FileStore/tables/asg1")
for i in range(2):
  dbutils.fs.cp("FileStore/tables/geoPoints"+str(i)+".csv","FileStore/tables/asg1")

# COMMAND ----------

sc = spark.sparkContext
import math
points = sc.textFile("FileStore/tables/asg1")
pointpairs = points.map(lambda x: x.split(',')).map(lambda x: (x[0],x[1:])).mapValues(lambda x: (float(x[0]),float(x[1])))
cellSize = sc.broadcast(1)

def grid_point(point):
  cellSize = 1
  x = point[1][0]
  y = point[1][1]
  xCell = math.floor(x//cellSize)
  yCell = math.floor(x//cellSize)
  return ((xCell,yCell),point)

def cc(value):
  return [value]

def mv(prev,value):
  prev.append(value)
  return prev

def mc(prev1,prev2):
  prev1.extend(prev2)
  return prev1

#map each point to its own cell
gridpointRDD = pointpairs.map(grid_point)

#map each cell to its adjacent cells
def maptoadj(pair):
  cell = pair[0]
  point = pair[1]
  oldx = cell[0]
  oldy = cell[1]
  right = (oldx+1,oldy)
  lowleft = (oldx-1,oldy-1)
  low = (oldx,oldy-1)
  lowright = (oldx+1,oldy-1)
  return [pair,(right,point),(lowleft,point),(low,point),(lowright,point)]

#euclidean distance function
def dist(pt1,pt2):
  return math.sqrt((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2)

def computeDist(points,maxdist):
  closepoints = []
  count = 0
  for i in points:
    for j in points:
      if i[1] == j[1]:
        continue
      distance = dist(i[1],j[1])
      if distance < maxdist and (j[0],i[0]) not in closepoints:
        #count += 1
        closepoints.append((i[0],j[0]))
  return closepoints

allcells = gridpointRDD.flatMap(maptoadj)
print()

#combine the values of each cell into one group
withincell = allcells.combineByKey(cc,mv,mc).map(lambda x: x[1]).persist()

dists = [x/10 for x in range(1,11)]

for i in dists:
  res = withincell.flatMap(lambda x: computeDist(x,i)).distinct()
  print("Dist: ",i)
  print(res.count(),res.collect())
  print()


# COMMAND ----------


