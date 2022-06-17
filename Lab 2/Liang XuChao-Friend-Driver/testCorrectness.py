from map import world
import random
from PyAgent import Agent
Maprow = 6
Mapcolumn = 7
portal = 3
coin = 1
wumpus =1
       

testinglist = [
["turnleft","moveforward"],
["moveforward","moveforward","moveforward","turnright","moveforward","moveforward","moveforward"],
["moveforward","moveforward","moveforward","turnright","shoot","turnleft"],
["moveforward","turnright","moveforward","moveforward","turnleft","moveforward","moveforward"],
["moveforward","turnright","moveforward","pickup"]

]
# hit border
#actions = ["turnleft","moveforward"]

# move to a wumpus and game over
#actions = ["moveforward","moveforward","moveforward","turnright","moveforward","moveforward","moveforward"]

# shoot arrow to wumpus
#actions = ["moveforward","moveforward","moveforward","turnright","shoot","turnleft"]

# move to a portal 
#actions = ["moveforward","turnright","moveforward","moveforward","turnleft","moveforward","moveforward"]

# pickup a coin
# actions = ["moveforward","turnright","moveforward","pickup"]
#print(actions)
outputfile = open("Quang-testPrintoutMove-Quang-XuChao.txt", "w")
for x in testinglist:
    pyAgent = Agent()

    outputfile.write("Generate World\n")

    ww = world(pyAgent,outputfile,Maprow,Mapcolumn,portal,coin,wumpus)
    portalfix = [[3,3],[4,3],[1,5]]
    coinsfix = [[2,2]]
    wumpusfix = [[4,2]]
    startpointfix = [1,1]
    absDirection = "anorth"
    ww.set_fixed_world_item(portalfix,coinsfix,wumpusfix,startpointfix,absDirection)
    print(ww.agentStartingPosition)
    ww.init_square()

    print("Print Absolute World")
    outputfile.write("Print Absolute World\n")
    ww.print_abs_world()

    outputfile.write("-------------------------------------------------------------------\n")

    pyAgent.reborn()

    print("Print initial sense")
    outputfile.write("Print initial sense\n")
    sense = ww.getSense(0,0,None,True)
    print(sense)
    pyAgent.reposition(sense)
    ww.updateUnknowWorld()


    print("Print initial Relative World")
    outputfile.write("Initial Relative World\n")
    print(ww.print_world("relative_unknow"))
    outputfile.write("-------------------------------------------------------------------\n")

    outputfile.write("Start testing\n")
    for i in x:
        rCoordBeforeMove = pyAgent.current()[0]
        sense = ww.getSense(rCoordBeforeMove["X"],rCoordBeforeMove["Y"],i,False)
        print(sense)
        pyAgent.move(i,sense)


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
                gameOver = True
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

outputfile.close()
