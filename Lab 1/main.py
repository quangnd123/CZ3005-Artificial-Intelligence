import json
from task1 import findMin 
from task2 import uniform_cost_search
from task3 import Astar

# PLEASE OPEN OUTPUT.TXT FILE TO SEE OUTPUT

g = open("G.json")
cost = open("Cost.json")
coord = open("Coord.json")
dist = open("Dist.json")
G = json.load(g)
Cost = json.load(cost)
Coord = json.load(coord)
Dist = json.load(dist)  

findMin("1","50",G,Dist,Cost)
uniform_cost_search("1","50",G,Dist,Cost,287932)
Astar("1","50",G,Dist,Cost,287932,Coord)

data1 = data2 = data3 =""
with open('task1output.txt') as fp:
    data1 = fp.read()
with open('task2output.txt') as fp:
    data2 = fp.read()
with open('task3output.txt') as fp:
    data3 = fp.read()
data  = data1 + data2 + data3
with open ('output.txt', 'w') as fp:
    fp.write(data)