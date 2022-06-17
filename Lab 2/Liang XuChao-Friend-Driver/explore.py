from map import world
import random
from PyAgent import Agent
Maprow = 6
Mapcolumn = 7
portal = 3
coin = 1
wumpus =1
       
pyAgent = Agent()
outputfile = open("Quang-testPrintoutExplore-Quang-XuChao.txt", "w")

outputfile.write("Generate World\n")

ww = world(pyAgent,outputfile,Maprow,Mapcolumn,portal,coin,wumpus)
ww.SetStarting_point()
print(ww.agentStartingPosition)
ww.generate_world_item()
ww.init_square()

print("Print Absolute World")
outputfile.write("Print Absolute World\n")
ww.print_abs_world()

outputfile.write("-------------------------------------------------------------------\n")
t = 0

pyAgent.reborn()
print("Print initial sense")
outputfile.write("Print initial sense\n")
sense = ww.getSense(0,0,None,True)
print(sense)
pyAgent.reposition(sense)
# ww.updateRelativeWorld()
ww.updateUnknowWorld()

gameEnd = False

print("Print initial Relative World")
outputfile.write("Initial Relative World\n")
# print(ww.print_world("relative"))
print(ww.print_world("relative_unknow"))
outputfile.write("-------------------------------------------------------------------\n")
#actions = pyAgent.Explore()[0]
while t < 1000 and gameEnd == False : 
    t+=1

    explore_path = pyAgent.explore()
    print(explore_path)
    actions = explore_path[0]
    print("explore(L):", actions['L'])
    if len(actions['L']) == 0:
        break
    # if len(actions['L'][0]['L']) == 0:
    #     break

    for i in actions['L']:
        
        rCoordBeforeMove = pyAgent.current()[0]
        # absoluteCoord = (ww.agentStartingPosition[1] + rCoordBeforeMove["X"], ww.agentStartingPosition[0] + rCoordBeforeMove["Y"])
        sense = ww.getSense(rCoordBeforeMove["X"],rCoordBeforeMove["Y"],i,False)
        pyAgent.move(i,sense)


        # ww.updateRelativeWorld()
        # print(ww.print_world("relative"))
        ww.updateUnknowWorld()
        print(ww.print_world("relative_unknow"))
        outputfile.write("-------------------------------------------------------------------\n")
        if i == "pickup":
            ww.updatePickupCoins()
        else:
            check =  ww.checkIfMoveToPortalOrWumpus()
            if check== "wumpus":
                print("move to wumpus")
                outputfile.write("Game Over\n")
                gameEnd = True
                break
            elif check == "portal":
                print("move to portal")
                outputfile.write("Step into portal, reposition...\n")
                ww.SetStarting_point()
                
                sense = ww.getSense(0,0,None,True)
                pyAgent.reposition(sense)
                ww.updateUnknowWorld()
                print(ww.print_world("relative_unknow"))
                outputfile.write("-------------------------------------------------------------------\n")
                break


outputfile.write("Print final absolute world\n")
ww.updateAbsoluteWorld()
print(ww.print_world("absolute"))
outputfile.write("-------------------------------------------------------------------\n")


outputfile.close()
