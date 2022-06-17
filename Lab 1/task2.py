def uniform_cost_search(start,end,G,Dist,Cost,maxCost):
    queue =[[0,0,-1,start]]
    memory=[]
    visited = []
    while(len(queue)>0):
        queue = sorted(queue)
        dist,cost,parent ,node = queue.pop()
        memory.append([dist,cost,parent ,node])
        dist =-dist
        if(node==end):
            s = end
            for i in range (len(memory)-1,-1,-1):
                if memory[i][3] == parent:
                    s = parent+ "->" + s
                    parent=memory[i][2]
            f = open("task2output.txt", "w")
            f.write('TASK 2:\n')
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
                if c <= maxCost:
                    queue.append([-d,c,node,G[node][i]])
        visited.append(node)

