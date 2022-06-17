from math import sqrt
def straightLineDist(Coord,x,y):
    x1 = Coord[x][0]
    y1 = Coord[x][1]
    x2 = Coord[y][0]
    y2 = Coord[y][1]
    return sqrt( pow(x1-x2,2) + pow(y1-y2,2))

def Astar(start,end,G,Dist,Cost,maxCost,Coord):
    queue =[[[start],0,0,-1,start]]
    memory=[]
    visited = []
    while(len(queue)>0):
        queue = sorted(queue)
        totalDist,dist, cost, parent ,node = queue.pop()
        memory.append([parent ,node])
        if(node==end):
            s = end
            for i in range (len(memory)-1,-1,-1):
                if memory[i][1] == parent:
                    s = parent+ "->" + s
                    parent=memory[i][0]
            f = open("task3output.txt", "w")
            f.write('TASK 3:\n')
            f.write("Shortest path: " +s +"\n")
            f.write("Shortest distance: {}".format(dist) +"\n")
            f.write("Total energy cost: {}".format(cost) +"\n\n")
            return
            
        if node in visited: 
            continue
        for i in range (len(G[node])):
            if G[node][i] not in visited:
                d = dist + Dist["{},{}".format(int(node),int(G[node][i]))]
                c = cost + Cost["{},{}".format(int(node),int(G[node][i]))]
                total = d + straightLineDist(Coord,end,"{}".format(G[node][i]))
                if c <= maxCost:
                    queue.append([-total,d,c,node,G[node][i]])
        visited.append(node)