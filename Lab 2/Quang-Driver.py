import re
from pyswip import Prolog

prolog = Prolog()
prolog.consult("Quang-Agent.pro")

wumpusRow = 3
wumpusCol = 3
confundusRow1 = 1
confundusCol1 = 2
confundusRow2 = 4
confundusCol2 = 4
confundusRow3 = 5
confundusCol3 = 4
coinRow1 = 1
coinCol1 = 1
hasarrow = True
minRelativeX = 0
maxRelativeX = 0
minRelativeY = 0
maxRelativeY = 0

#f = open("Quang-testPrintoutExplore-Self-Self.txt", "w")
f = open("Quang-testPrintoutMove-Self-Self.txt", "w")

def main():
    #start
    map = create_map()
    print_map(map)
    f.write("Start game:\n")
    X,Y,D,map=init()

    #Please uncomment line 23 and line 36 AND comment out line 24 and line 35 to use function explore
    
    test_move_function(X,Y,D,map)
    #explore(X,Y,D,map)

def explore(X,Y,D,map):
    while (1):
        L = list(prolog.query("explore(L)"))[0]["L"]
        if L==[]:
            f.write("No more safe location\n")
            break
        for action in L:
            X,Y,D,map=move(X,Y,D,"{action}".format(action=action),map)


def test_move_function(X,Y,D,map):
    # test reborn
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"turnright",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)

    #test reposition, pickup and shoot
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"turnright",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"pickup",map)
    X,Y,D,map=move(X,Y,D,"turnleft",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"turnleft",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"turnleft",map)
    X,Y,D,map=move(X,Y,D,"moveforward",map)
    X,Y,D,map=move(X,Y,D,"shoot",map)

def move(X,Y,D,action,map):
    f.write("Action: ")
    f.write(action)
    f.write("\n")
    X,Y,D,Bump,Confundus,Wumpus=update_absolute_position(X,Y,D,action,map)
    sense = sensory(X,Y,D,action,map)
    if Bump:
        sense[4]="on"
    if Confundus:
        sense[0]="on"
    update_min_max_Relative()
    print_sensory(sense)
    print_map(map)
    list(prolog.query("move({action},{sense})".format(action=action,sense=sense)))
    print_relative_map(sense)
    if sense[0]=="on":
        X,Y,D,map=reposition()
    if Wumpus:
        f.write("You were eaten by Wumpus!\n")
        f.write("Start game again!\n")
        X,Y,D,map = init()
    return X,Y,D,map

def print_sensory(sense):
    f.write("Sensory: ")
    if sense[0]=="on":
        f.write("Confounded-")
    else:
        f.write("C-")
    if sense[1]=="on":
        f.write("Stench-")
    else:
        f.write("S-")
    if sense[2]=="on":
        f.write("Tingle-")
    else:
        f.write("T-")
    if sense[3]=="on":
        f.write("Glitter-")
    else:
        f.write("G-")
    if sense[4]=="on":
        f.write("Bump-")
    else:
        f.write("B-")
    if sense[5]=="on":
        f.write("Scream")
    else:
        f.write("S")
    f.write("\n")

def init():
    X=1
    Y=5 
    D="north"
    map = create_map()
    update_agent_map(X,Y,D,map)
    sense = sensory(X,Y,D,"start",map)
    sense[0]="on"
    reset_min_max_Relative()
    print_map(map)
    list(prolog.query("reborn"))
    list(prolog.query("reposition({sense})".format(sense=sense)))
    print_relative_map(sense)
    return X,Y,D,map

def reposition():
    X=1
    Y=2
    D="north"
    map = create_map()
    update_agent_map(X,Y,D,map)
    sense = sensory(X,Y,D,"relocate",map)
    sense[0]="on"
    reset_min_max_Relative()
    print_sensory(sense)
    print_map(map)
    list(prolog.query("reposition({sense})".format(sense=sense)))
    print_relative_map(sense)
    return X,Y,D,map

def update_absolute_position(X,Y,D,action,map):
    map[Y][X][1][0]=" "
    map[Y][X][1][2]=" "
    map[Y][X][1][1]="S"
    Bump = False
    Wumpus = False
    Confundus = False
    if action=="turnright":
        if D =="north": 
            D="east"
        elif D =="east": 
            D="south"
        elif D =="south": 
            D="west"
        else : 
            D="north"
    elif action=="turnleft":
        if D =="north": 
            D="west"
        elif D =="west": 
            D="south"
        elif D =="south": 
            D="east"
        else : 
            D="north"
    elif action=="moveforward":
        if not checkWallfront(X,Y,D,map):
            if D =="north": 
                Y=Y-1
            elif D =="east": 
                X=X+1
            elif D =="south": 
                Y=Y+1
            else : 
                X=X-1
        else: 
            Bump=True
    elif action=="pickup":
        map[Y][X][2][0]="."
    elif action=="shoot" and hasarrow:
        if D=="north" and wumpusCol==X and wumpusRow<Y:
            killWumpus(map)
        if D=="east" and wumpusRow==Y and wumpusCol>X:
            killWumpus(map)
        if D=="south" and wumpusCol==X and wumpusRow>Y:
            killWumpus(map)
        if D=="west" and wumpusCol==Y and wumpusCol<X:
            killWumpus(map)
    
    if map[Y][X][1][1]=="O":
        Confundus=True
    elif map[Y][X][1][1]=="W":
        Wumpus=True
    update_agent_map(X,Y,D,map)
    return X,Y,D,Bump,Confundus,Wumpus

def killWumpus(map):
    map[wumpusRow][wumpusCol][1][1]='s'
    map[wumpusRow][wumpusCol][1][0]=' '
    map[wumpusRow][wumpusCol][1][2]=' '

    map[wumpusRow+1][wumpusCol][0][1]="."
    map[wumpusRow-1][wumpusCol][0][1]="."
    map[wumpusRow][wumpusCol+1][0][1]="."
    map[wumpusRow][wumpusCol-1][0][1]="."

def update_agent_map(X,Y,D,map):
    if D=="north":
        map[Y][X][1][1]="^"
    elif D=="east":
        map[Y][X][1][1]=">"
    elif D=="south":
        map[Y][X][1][1]="v"
    else:
        map[Y][X][1][1]="<"
    map[Y][X][1][0]="-"
    map[Y][X][1][2]="-"


def checkWallfront(X,Y,D,map):
    if D=="north" and map[Y-1][X][0][0]=="#":
        return True
    if D=="east" and map[Y][X+1][0][0]=="#":
        return True
    if D=="south" and map[Y+1][X][0][0]=="#":
        return True
    if D=="west" and map[Y][X-1][0][0]=="#":
        return True

def update_min_max_Relative():
    relativePosition = list(prolog.query("current(X,Y,D)"))[0]
    relativeX = relativePosition["X"]
    relativeY = relativePosition["Y"]
    listOfGlobals = globals()
    if relativeX<listOfGlobals['minRelativeX']:
        listOfGlobals['minRelativeX'] = relativeX
    if relativeX>listOfGlobals['maxRelativeX']:
        listOfGlobals['maxRelativeX'] = relativeX

    if relativeY<listOfGlobals['minRelativeY']:
        listOfGlobals['minRelativeY'] = relativeY
    if relativeY>listOfGlobals['maxRelativeY']:
        listOfGlobals['maxRelativeY'] = relativeY

def reset_min_max_Relative():
    listOfGlobals = globals()
    listOfGlobals['minRelativeX']=0
    listOfGlobals['maxRelativeX']=0
    listOfGlobals['minRelativeY']=0
    listOfGlobals['maxRelativeY']=0

def sensory(X,Y,D,action,map):
    Confounded="off"
    Stench="off"
    Tingle="off"
    Glitter="off"
    Bump="off"
    Scream="off"
    # End = "no"
    # if map[Y][X][1][1]=="W":
    #     End = "yes"
    if map[Y][X][1][1]=="O":
        Confounded="on"
    if map[Y][X][0][1]=="=":
        Stench="on"
    if map[Y][X][0][2]=="T":
        Tingle="on"
    if map[Y][X][2][0]=="*":
        Glitter="on"
    if action =="shoot" and hasarrow:
        if D=="north" and wumpusCol==X and wumpusRow<Y:
            Scream="on"
        if D=="east" and wumpusRow==Y and wumpusCol>X:
            Scream="on"
        if D=="south" and wumpusCol==X and wumpusRow>Y:
            Scream="on"
        if D=="west" and wumpusCol==Y and wumpusCol<X:
            Scream="on"
        listOfGlobals = globals()
        listOfGlobals['hasarrow'] =False
    if map[Y][X][0][0]=="#":
        Bump="on"
    return [Confounded,Stench,Tingle,Glitter,Bump,Scream]

def create_map():
    map = [[ [[".",".","."],[" ","s"," "],[".",".","."]] for col in range(6)] for row in range (7)]
    
    #create wumpus
    map[wumpusRow][wumpusCol] = [[".",".","."],["-","W","-"],[".",".","."]]
    
    #create confundus
    map[confundusRow1][confundusCol1] = [[".",".","."],["-","O","-"],[".",".","."]]

    map[confundusRow2][confundusCol2] = [[".",".","."],["-","O","-"],[".",".","."]]

    map[confundusRow3][confundusCol3] = [[".",".","."],["-","O","-"],[".",".","."]]

    #create coins
    map[coinRow1][coinCol1] = [[".",".","."],[" ","s"," "],["*",".","."]]

    #create stench
    map[wumpusRow+1][wumpusCol][0][1]="="
    map[wumpusRow-1][wumpusCol][0][1]="="
    map[wumpusRow][wumpusCol+1][0][1]="="
    map[wumpusRow][wumpusCol-1][0][1]="="

    #create tingle
    map[confundusRow1+1][confundusCol1][0][2] = "T"
    map[confundusRow1-1][confundusCol1][0][2] = "T"
    map[confundusRow1][confundusCol1+1][0][2] = "T"
    map[confundusRow1][confundusCol1-1][0][2] = "T"

    map[confundusRow2+1][confundusCol2][0][2] = "T"
    map[confundusRow2-1][confundusCol2][0][2] = "T"
    map[confundusRow2][confundusCol2+1][0][2] = "T"
    map[confundusRow2][confundusCol2-1][0][2] = "T"

    map[confundusRow3+1][confundusCol3][0][2] = "T"
    map[confundusRow3-1][confundusCol3][0][2] = "T"
    map[confundusRow3][confundusCol3+1][0][2] = "T"
    map[confundusRow3][confundusCol3-1][0][2] = "T"

    #create outer walls
    for i in range(6):
        map[0][i] =[["#","#","#"],["#","#","#"],["#","#","#"]]
        map[6][i] =[["#","#","#"],["#","#","#"],["#","#","#"]]
    for i in range(7):
        map[i][0] =[["#","#","#"],["#","#","#"],["#","#","#"]]
        map[i][5] =[["#","#","#"],["#","#","#"],["#","#","#"]]

    return map

def print_map(map):
    f.write("Absolute map:\n")
    for row in range(21):
        for col in range(18):
            CellY= int(row/3)
            CellX= int(col/3)
            RelativeY= row%3
            RelativeX= col%3
            f.write(map[CellY][CellX][RelativeY][RelativeX]) 
            f.write(" ")
        f.write("\n")
    f.write("\n")

def print_relative_map(sense):
    f.write("Relative map:\n")
    relativePosition = list(prolog.query("current(X,Y,D)"))[0]
    relativeX = relativePosition["X"]
    relativeY = relativePosition["Y"]
    relativeD = relativePosition["D"]
    if relativeX-minRelativeX>=maxRelativeX-relativeX:
        DX = relativeX-minRelativeX
    else: 
        DX = maxRelativeX-relativeX
    if relativeY-minRelativeY>=maxRelativeY-relativeY:
        DY = relativeY-minRelativeY
    else: 
        DY = maxRelativeY-relativeY
    EndX = (DX+1)*6+3
    EndY = (DY+1)*6+3
    for StartY in range(EndY):
        for StartX in range (EndX):
            CellX=StartX//3+relativeX-EndX//6
            CellY = EndY//6-StartY//3+relativeY
            positionXinCell = StartX%3
            positionYinCell = StartY%3
            Cell = {'X':CellX,'Y':CellY}

            CellisRelativePosition = relativeX == CellX and relativeY==CellY

            wallList = list(prolog.query("wall(X,Y)"))
            glitterList = list(prolog.query("glitter(X,Y)"))
            wumpusList = list(prolog.query("wumpus(X,Y)"))
            confundusList = list(prolog.query("confundus(X,Y)"))
            visitedList = list(prolog.query("visited(X,Y)"))
            safeUnvisitedList=list(prolog.query("safe(X,Y),\+visited(X,Y)"))
            if Cell in wallList:
                f.write("# ")
                continue
            if positionYinCell==0 and positionXinCell==0:
                if sense[0]=="on" and CellisRelativePosition:
                    f.write("%")
                else :
                    f.write(".")
            elif positionYinCell==0 and positionXinCell==1:
                if sense[1]=="on" and CellisRelativePosition:
                    f.write("=")
                else :
                    f.write(".")
            elif positionYinCell==0 and positionXinCell==2:
                if sense[2]=="on" and CellisRelativePosition:
                    f.write("T")
                else :
                    f.write(".")
            elif positionYinCell==1 and (positionXinCell==0 or positionXinCell==2):
                if CellisRelativePosition or Cell in glitterList or Cell in wumpusList or Cell in confundusList:
                    f.write('-')
                else :
                    f.write('.')
            elif positionYinCell==1 and positionXinCell==1:
                if CellisRelativePosition:
                    if relativeD=="rnorth":
                        f.write('^')
                    elif relativeD=="reast":
                        f.write('>')
                    elif relativeD=="rsouth":
                        f.write('v')
                    else:
                        f.write('<')
                elif Cell in visitedList:
                    f.write('S')
                elif Cell in safeUnvisitedList:
                    f.write('s')
                elif Cell in wumpusList and Cell in confundusList:
                    f.write('U')
                elif Cell in wumpusList:
                    f.write('W')
                elif Cell in confundusList:
                    f.write('O')
                else :
                    f.write('?')
            elif positionYinCell==2 and positionXinCell==0:
                if CellisRelativePosition and sense[3]=="on":
                    f.write('*')
                else :
                    f.write('.')
            elif positionYinCell==2 and positionXinCell==1:
                if CellisRelativePosition and sense[4]=="on":
                    f.write('B')
                else :
                    f.write('.')
            else :
                if CellisRelativePosition and sense[5]=="on":
                    f.write('@')
                else :
                    f.write('.')
            f.write(" ")
        f.write("\n")
    f.write("\n")
main()