
import random
from re import I
import sys
from unittest import skip
# portal = "P"
# start = "S"
# coins = "C"
# wumpus = "W"
# border = "B"
class world():

    def __init__(self, pyAgent, outputfile, row, column, portalCount = 3, coinsCount = 1, wumpusCount = 1):
        self.worldArr = []
        self.agentStartingPosition = []
        self.AbsoluteWorldArr = []
        self.RelativeWorldUnknownArr = []
        self.portalCount = portalCount
        self.coinsCount = coinsCount
        self.wumpusCount = wumpusCount
        self.row = row
        self.column = column
        self.portals = []
        self.wumpus = []
        self.coins = []
        self.Tingle = {}    # stores locations of breezy squares
        self.Stench = {}
        self.pyAgent = pyAgent
        self.outputfile = outputfile
        self.absDirection = ""
        self.agentStartingDirection = ""
        self.wumpusDefeated = False
        

        for r in range(0,row):
            rowlist = []

            for c in range(0,column):
                if (r == 0) or (r == (row-1)) or (c==0) or (c== (column-1)):
                    rowlist.append("B")
                else:
                    rowlist.append(0)
            
            self.worldArr.append(rowlist)

        self.resetAbsoluteWorldArr()

    def resetAbsoluteWorldArr(self):
        self.AbsoluteWorldArr = []
        for r in range(0,self.row):
            rowlist = []

            for c in range(0,self.column):
                rowlist.append([".",".","."," ","?"," ",".",".","."])
            
            self.AbsoluteWorldArr.append(rowlist)
    
    def set_fixed_world_item(self,portal,coins,wumpus,startpoint,direction):
        for i in portal:
            self.worldArr[i[0]][i[1]] = "P"
            self.portals.append((i[0],i[1]))
        
        for i in coins:
            self.worldArr[i[0]][i[1]] = "C"
            self.coins.append([i[0],i[1],"ND"])

        for i in wumpus:
            self.worldArr[i[0]][i[1]] = "W"
            self.wumpus.append((i[0],i[1]))

        self.agentStartingPosition = [startpoint[0],startpoint[1]]
        self.worldArr[startpoint[0]][startpoint[1]] = "S"
        self.absDirection = direction
        self.agentStartingDirection = direction


    def generate_world_item(self):
        
        #generate portal
        for pc in range(0,self.portalCount):
            row,col = self.get_random_location()
            self.worldArr[row][col] = "P"
            self.portals.append((row,col))
        
        #generate coins
        for cc in range(0,self.coinsCount):
            row,col = self.get_random_location()
            self.worldArr[row][col] = "C"
            self.coins.append([row,col,"ND"])

        #generate wumpus
        for wc in range(0,self.wumpusCount):
            row,col = self.get_random_location()
            self.worldArr[row][col] = "W"
            self.wumpus.append((row,col))
    
    def get_random_location(self):
        row = random.randint(0,self.row-1)
        col = random.randint(0,self.column-1)
        while (self.worldArr[row][col] != 0):
            row = random.randint(0,self.row-1)
            col = random.randint(0,self.column-1)
        
        return row,col
        
    def SetStarting_point(self):
        row = random.randint(1, self.row-2)
        col = random.randint(1, self.column-2)
        while (self.worldArr[row][col] == "W" or self.worldArr[row][col] == "B" or self.worldArr[row][col] == "P"):
            row = random.randint(1, self.row-2)
            col = random.randint(1, self.column-2)
        self.agentStartingPosition = [row,col]
        self.worldArr[row][col] = "S"
        

        direction = ["anorth","asouth","aeast","awest"]
        randomindex = random.randint(0, 3)
        self.absDirection = direction[randomindex]
        self.agentStartingDirection = direction[randomindex]
       

    def print_world(self,type):
        arr = []
        if type == "absolute":
            arr = self.AbsoluteWorldArr
        elif type == "relative_unknow":
            arr = self.RelativeWorldUnknownArr
        self.format_world(arr)
        

    def format_world(self,arr):
        out = "+"
        for c in range(0, len(arr[0])):
            out += "---+"
        print(out)
        self.outputfile.write(out + "\n")

        for r in range(len(arr)-1, -1, -1):
            out = "|"
            for c in range(0,len(arr[r])):
                
                out +=arr[r][c][0]
                out +=arr[r][c][1]
                out +=arr[r][c][2]
                out += "|"
            print(out)
            self.outputfile.write(out + "\n")      

            out = "|"
            for c in range(0,len(arr[r])):
                out +=arr[r][c][3]
                out +=arr[r][c][4]
                out +=arr[r][c][5]
                out += "|"
            print(out)
            self.outputfile.write(out + "\n") 

            out = "|"
            for c in range(0,len(arr[r])):
                out +=arr[r][c][6]
                out +=arr[r][c][7]
                out +=arr[r][c][8]
                out += "|"
            print(out)
            self.outputfile.write(out + "\n")           

            out = "+"
            for c in range(0, len(arr[0])):
                out += "---+"
            print(out)
            self.outputfile.write(out + "\n")  
        return
            

    def print_abs_world(self):
        # print("World size = {}x{}".format(self.row, self.column))

        # print out the first horizontal line
        out = "+"
        for c in range(0, self.column):
            out += "---+"
        print(out)
        self.outputfile.write(out + "\n")
        
        for r in range(self.row-1, -1, -1):  # print starting from the 'bottom' up
            
            out = "|"

            for c in range(0, self.column):
                out += " "
                if self.worldArr[r][c] == "C":
                    out += "C"
                elif self.worldArr[r][c] == "W":
                    out += "W"
                elif self.worldArr[r][c] == "P":
                    out += "P"
                elif self.worldArr[r][c] == "S":
                    out += "S"
                elif self.worldArr[r][c] == "B":
                    out += "B"
                else:
                    out += " "
                out += " "
                out += "|"
            print(out)   
            self.outputfile.write(out + "\n")

            out = "+"
            for c in range(0, self.column):
                out += "---+"
            print(out)
            self.outputfile.write(out + "\n") 

    
    def changeStart(self,r,c):
        self.worldArr[r][c] == "S"

    def init_square(self):
        for p in self.portals: # initalise breezy squares
            for l in self.neighbours(p):
                self.Tingle[l] = True
        for w in self.wumpus: # intialise smelly squares
            for l in self.neighbours(w):
                self.Stench[l] = True

    def neighbours(self, loc):    # returns neighbours of tuple loc = (x,y) 
        return [(loc[0]+1,loc[1]), (loc[0]-1,loc[1]), (loc[0],loc[1]+1), (loc[0],loc[1]-1)]

     

    def getSense(self,rCoordx,rCoordy,action=None,start=False):
        sense = ["off","off","off","off","off","off"]

        self.outputfile.write("Absolute direction on map: " + self.absDirection + "\n")
        self.outputfile.write("Action: " + str(action) + "\n")
        if action == "turnleft":
            if self.absDirection == "anorth":
                self.absDirection = "awest"
            elif self.absDirection == "asouth":
                self.absDirection = "aeast"
            elif self.absDirection == "aeast":
                self.absDirection = "anorth"
            elif self.absDirection == "awest":
                self.absDirection = "asouth"
        elif action == "turnright":
            if self.absDirection == "anorth":
                self.absDirection = "aeast"
            elif self.absDirection == "asouth":
                self.absDirection = "awest"
            elif self.absDirection == "aeast":
                self.absDirection = "asouth"
            elif self.absDirection == "awest":
                self.absDirection = "anorth"


        if self.agentStartingDirection == "anorth":
            r = self.agentStartingPosition[0] + rCoordy
            c = self.agentStartingPosition[1] + rCoordx
        elif self.agentStartingDirection == "asouth": 
            r = self.agentStartingPosition[0] - rCoordy
            c = self.agentStartingPosition[1] - rCoordx
        elif self.agentStartingDirection == "aeast": 
            r = self.agentStartingPosition[0] - rCoordx
            c = self.agentStartingPosition[1] + rCoordy
        elif self.agentStartingDirection == "awest": 
            r = self.agentStartingPosition[0] + rCoordx
            c = self.agentStartingPosition[1] - rCoordy
        

        self.outputfile.write("Absolute direction on map after move: " + str(self.absDirection) + "\n")

        if start:
            sense[0] = "on"


        if action != "moveforward":

            Tingle = (r,c) in self.Tingle
            Stench = (r,c) in self.Stench
            if Tingle:
                sense[2] = "on"
            
            if Stench:
                sense[1] = "on"
            
        else:
            newr = r
            newc = c
            if self.absDirection == "anorth" and r-1 < self.row:
                newr = r+1
                newc = c

            elif self.absDirection == "asouth" and r+1 >= 0:
                newr = r-1
                newc = c

            elif self.absDirection == "awest" and c+1 >= 0:
                newr = r
                newc = c-1

            elif self.absDirection == "aeast" and c-1 < self.column:
                newr = r
                newc = c+1

            Tingle = (newr,newc) in self.Tingle
            Stench = (newr,newc) in self.Stench
            GlitterNotDetected = [newr,newc,"ND"] in self.coins
            GlitterNotPick = [newr,newc,"D"] in self.coins
            print(self.coins)
            print(GlitterNotDetected)
            print(GlitterNotPick)
            self.outputfile.write("Coins Data: " + str(self.coins) + "\n")

            if Tingle:
                sense[2] = "on"
            
            if Stench:
                sense[1] = "on"
                
            if GlitterNotDetected or GlitterNotPick:
                sense[3] = "on"

        
        # print("sense: " + direction + " " + str(r) + " " + str(c))
        if action == "moveforward" and self.absDirection == "anorth" and r-1 < self.row:
            if self.worldArr[r+1][c] == "B":
                sense[4] = "on"

        elif action == "moveforward" and self.absDirection == "asouth" and r+1 >= 0:
            if self.worldArr[r-1][c] == "B":
                sense[4] = "on"

        elif action == "moveforward" and self.absDirection == "awest" and c+1 >= 0:
            if self.worldArr[r][c-1] == "B":
                sense[4] = "on"

        elif action == "moveforward" and self.absDirection == "aeast" and c-1 < self.column:
            if self.worldArr[r][c+1] == "B":
                sense[4] = "on"

        if action == "shoot" and self.absDirection == "anorth" and r-1 < self.row:
            for i in range(1,self.row-1-r):
                if self.worldArr[r+i][c] == "W":
                    self.wumpusDefeated = True
                    self.Stench = []
                    sense[5] = "on"
                    break

        elif action == "shoot" and self.absDirection == "asouth" and r+1 >= 0:
            for i in range(1,r+1):
                if self.worldArr[r-i][c] == "W":
                    self.wumpusDefeated = True
                    self.Stench = []
                    sense[5] = "on"
                    break

        elif action == "shoot" and self.absDirection == "awest" and c+1 >= 0:
            for i in range(1,c+1):
                if self.worldArr[r][c-i] == "W":
                    self.wumpusDefeated = True
                    self.Stench = []
                    sense[5] = "on"
                    break
           
        elif action == "shoot" and self.absDirection == "aeast" and c-1 < self.column:
            for i in range(1,self.column-1-c):
                if self.worldArr[r][c+i] == "W":
                    self.wumpusDefeated = True
                    self.Stench = []
                    sense[5] = "on"
                    break
           

        outprint = ""
        if sense[0] == "on":
            outprint += "Confounded-"
        else:
            outprint += "C-"

        if sense[1] == "on":
            outprint += "Stench-"
        else:
            outprint += "S-"

        if sense[2] == "on":
            outprint += "Tingle-"
        else:
            outprint += "T-"

        if sense[3] == "on":
            outprint += "Glitter-"
        else:
            outprint += "G-"

        if sense[4] == "on":
            outprint += "Bump-"
        else:
            outprint += "B-"

        if sense[5] == "on":
            outprint += "Scream-"
        else:
            outprint += "S-"
            #Confounded-Stench-T-Glitter-BS
        self.outputfile.write("Sensory Data: " + outprint[:-1] + "\n")
        print(outprint[:-1])
        return sense

    def updateAbsoluteWorld(self):
        rCoord = self.pyAgent.current()
        visited =  self.pyAgent.visited()
        wumpus =  self.pyAgent.wumpus()
        confundus =  self.pyAgent.confundus()
        tingle =  self.pyAgent.tingle()
        glitter =  self.pyAgent.glitter()
        stench =  self.pyAgent.stench()
        safe =  self.pyAgent.safe()
        wall =  self.pyAgent.wall()

        self.outputfile.write("Agent current coordinate: --- " + str(rCoord) +"\n")
        self.outputfile.write("Agent visited coordinate: --- " + str(visited) +"\n")
        self.outputfile.write("Agent wumpus coordinate: --- " + str(wumpus) +"\n")
        self.outputfile.write("Agent confundus coordinate: --- " + str(confundus) +"\n")
        self.outputfile.write("Agent tingle coordinate: --- " + str(tingle) +"\n")
        self.outputfile.write("Agent glitter coordinate: --- " + str(glitter) +"\n")
        self.outputfile.write("Agent stench coordinate: --- " + str(stench) +"\n")
        self.outputfile.write("Agent safe coordinate: --- " + str(safe) +"\n")
        self.outputfile.write("Agent wall coordinate: --- " + str(wall) +"\n")
        Astartpoint = self.agentStartingPosition
        print(Astartpoint)

        
        confList = []

        for i in confundus:
            absRow,absColumn = self.getAbsRowAndColumn(i)
            self.AbsoluteWorldArr[absRow][absColumn][4] = "O"
            confList.append((absRow,absColumn))

        for i in wumpus:
            absRow,absColumn = self.getAbsRowAndColumn(i)
            
            symbol = "W"
            for x in confList:
                if x[0] == absRow and x[1] == absColumn:
                    symbol = "U"
                    break

            self.AbsoluteWorldArr[absRow][absColumn][4] = symbol
            
        for i in safe:
            absRow,absColumn = self.getAbsRowAndColumn(i)
            if absRow < self.row and absRow >= 0 and absColumn >= 0 and self.column > absColumn:
                self.AbsoluteWorldArr[absRow][absColumn][4] = "s"

            # wumpusList.append((absRow,absColumn))

        

        for i in visited:
            absRow,absColumn = self.getAbsRowAndColumn(i)
            self.AbsoluteWorldArr[absRow][absColumn][4] = "S"
            
       
        CurrentRow,CurrentColumn = self.getAbsRowAndColumn(rCoord[0])
        CurrentDirection = self.absDirection
        arrow = ""
        if CurrentDirection == "anorth":
            arrow = "^"
        elif CurrentDirection == "asouth":
            arrow = "V"
        elif CurrentDirection == "aeast":
            arrow = ">"
        elif CurrentDirection == "awest":
            arrow = "<"
        self.AbsoluteWorldArr[CurrentRow][CurrentColumn][4] = arrow
        self.AbsoluteWorldArr[CurrentRow][CurrentColumn][3] = "-"
        self.AbsoluteWorldArr[CurrentRow][CurrentColumn][5] = "-"

        if rCoord[0]["Y"] == 0 and rCoord[0]["X"] == 0:
            absRow = Astartpoint[0]
            absColumn = Astartpoint[1]
            self.AbsoluteWorldArr[absRow][absColumn][0] = "%"

        for i in stench:
            absRow,absColumn = self.getAbsRowAndColumn(i)
            self.AbsoluteWorldArr[absRow][absColumn][1] = "="

        for i in tingle:
            absRow,absColumn = self.getAbsRowAndColumn(i)
            self.AbsoluteWorldArr[absRow][absColumn][2] = "T"

        
        for i in glitter:
            absRow,absColumn = self.getAbsRowAndColumn(i)
            self.AbsoluteWorldArr[absRow][absColumn][6] = "*"
            self.AbsoluteWorldArr[absRow][absColumn][3] = "-"
            self.AbsoluteWorldArr[absRow][absColumn][5] = "-"

        for i in wall:
            absRow,absColumn = self.getAbsRowAndColumn(i)
            self.AbsoluteWorldArr[absRow][absColumn][0] = "#"
            self.AbsoluteWorldArr[absRow][absColumn][1] = "#"
            self.AbsoluteWorldArr[absRow][absColumn][2] = "#"
            self.AbsoluteWorldArr[absRow][absColumn][3] = "#"
            self.AbsoluteWorldArr[absRow][absColumn][4] = "#"
            self.AbsoluteWorldArr[absRow][absColumn][5] = "#"
            self.AbsoluteWorldArr[absRow][absColumn][6] = "#"
            self.AbsoluteWorldArr[absRow][absColumn][7] = "#"
            self.AbsoluteWorldArr[absRow][absColumn][8] = "#"

        return 
    
    
    def updateUnknowWorld(self):
        
        rCoord = self.pyAgent.current()
        visited =  self.pyAgent.visited()
        wumpus =  self.pyAgent.wumpus()
        confundus =  self.pyAgent.confundus()
        tingle =  self.pyAgent.tingle()
        glitter =  self.pyAgent.glitter()
        stench =  self.pyAgent.stench()
        safe =  self.pyAgent.safe()
        wall =  self.pyAgent.wall()
        # certainwumpus =  self.pyAgent.certainwumpus()

        self.outputfile.write("Agent current coordinate: --- " + str(rCoord) +"\n")
        self.outputfile.write("Agent visited coordinate: --- " + str(visited) +"\n")
        self.outputfile.write("Agent wumpus coordinate: --- " + str(wumpus) +"\n")
        self.outputfile.write("Agent confundus coordinate: --- " + str(confundus) +"\n")
        self.outputfile.write("Agent tingle coordinate: --- " + str(tingle) +"\n")
        self.outputfile.write("Agent glitter coordinate: --- " + str(glitter) +"\n")
        self.outputfile.write("Agent stench coordinate: --- " + str(stench) +"\n")
        self.outputfile.write("Agent safe coordinate: --- " + str(safe) +"\n")
        self.outputfile.write("Agent wall coordinate: --- " + str(wall) +"\n")
        # self.outputfile.write("Agent certain wumpus coordinate: --- " + str(certainwumpus) +"\n")

        smallestX = 0
        smallestY = 0
        largestX = 0
        largestY = 0

        def findSize(object):
            nonlocal smallestX
            nonlocal smallestY
            nonlocal largestX
            nonlocal largestY
            for i in object:
                if i["X"] < smallestX:
                    smallestX = i["X"]
                elif i["X"] > largestX:
                    largestX = i["X"]

                if i["Y"] < smallestY:
                    smallestY = i["Y"]
                elif i["Y"] > largestY:
                    largestY = i["Y"]
            
        findSize(visited)
        findSize(wumpus)
        findSize(confundus)
        findSize(tingle)
        findSize(glitter)
        findSize(stench)
        findSize(safe)
        findSize(wall)
        
        xlength = largestX - smallestX + 1
        ylength = largestY - smallestY + 1

        Astartpoint = [0-smallestY,0-smallestX]
        # print(Astartpoint)


        relativeMap = []
        for r in range(0,ylength):
            rowlist = []

            for c in range(0,xlength):
                rowlist.append([".",".","."," ","?"," ",".",".","."])
            
            relativeMap.append(rowlist)

        # print(relativeMap)

        
        if rCoord[0]["Y"] == 0 and rCoord[0]["X"] == 0:
            absRow = Astartpoint[0]
            absColumn = Astartpoint[1]
            relativeMap[absRow][absColumn][0] = "%"

        confList = []
        for i in confundus:
            absRow = Astartpoint[0] + i["Y"]
            absColumn = Astartpoint[1] + i["X"]
            relativeMap[absRow][absColumn][4] = "O"
            confList.append((absRow,absColumn))

        for i in wumpus:
            absRow = Astartpoint[0] + i["Y"]
            absColumn = Astartpoint[1] + i["X"]

            symbol = "W"
            for x in confList:
                if x[0] == absRow and x[1] == absColumn:
                    symbol = "U"
                    break

            relativeMap[absRow][absColumn][4] = symbol

        for i in safe:
            absRow = Astartpoint[0] + i["Y"]
            absColumn = Astartpoint[1] + i["X"]
            # print(absColumn)
            # print(absRow)
            if absRow < self.row and absRow >= 0 and absColumn >= 0 and self.column > absColumn:
                relativeMap[absRow][absColumn][4] = "s"

        for i in visited:
            absRow = Astartpoint[0] + i["Y"]
            absColumn = Astartpoint[1] + i["X"]
            relativeMap[absRow][absColumn][4] = "S"
            
       
        CurrentRow = Astartpoint[0] + rCoord[0]["Y"]
        CurrentColumn = Astartpoint[1] + rCoord[0]["X"]
        CurrentDirection = rCoord[0]["D"]
        arrow = ""
        if CurrentDirection == "rnorth":
            arrow = "^"
        elif CurrentDirection == "rsouth":
            arrow = "V"
        elif CurrentDirection == "reast":
            arrow = ">"
        elif CurrentDirection == "rwest":
            arrow = "<"
        relativeMap[CurrentRow][CurrentColumn][4] = arrow
        relativeMap[CurrentRow][CurrentColumn][3] = "-"
        relativeMap[CurrentRow][CurrentColumn][5] = "-"

        for i in stench:
            absRow = Astartpoint[0] + i["Y"]
            absColumn = Astartpoint[1] + i["X"]
            relativeMap[absRow][absColumn][1] = "="

        for i in tingle:
            absRow = Astartpoint[0] + i["Y"]
            absColumn = Astartpoint[1] + i["X"]
            relativeMap[absRow][absColumn][2] = "T"

        
        for i in glitter:
            absRow = Astartpoint[0] + i["Y"]
            absColumn = Astartpoint[1] + i["X"]
            relativeMap[absRow][absColumn][6] = "*"
            relativeMap[absRow][absColumn][3] = "-"
            relativeMap[absRow][absColumn][5] = "-"

            r,c = self.getAbsRowAndColumn(i)
            for y in range(0,len(self.coins)):
                if r == self.coins[y][0] and c == self.coins[y][1]:
                    self.coins[y][2] = "D"
                    break

        for i in wall:
            absRow = Astartpoint[0] + i["Y"]
            absColumn = Astartpoint[1] + i["X"]
            relativeMap[absRow][absColumn][0] = "#"
            relativeMap[absRow][absColumn][1] = "#"
            relativeMap[absRow][absColumn][2] = "#"
            relativeMap[absRow][absColumn][3] = "#"
            relativeMap[absRow][absColumn][4] = "#"
            relativeMap[absRow][absColumn][5] = "#"
            relativeMap[absRow][absColumn][6] = "#"
            relativeMap[absRow][absColumn][7] = "#"
            relativeMap[absRow][absColumn][8] = "#"
        self.RelativeWorldUnknownArr = relativeMap

    def checkIfMoveToPortalOrWumpus(self):
        
        rCoord = self.pyAgent.current()[0]
        r,c = self.getAbsRowAndColumn(rCoord)

        print(self.worldArr[r][c])
        if self.worldArr[r][c] == "P":
            return "portal"
        elif self.worldArr[r][c] == "W" and self.wumpusDefeated == False:
            return "wumpus"

    def updatePickupCoins(self):
        rCoord = self.pyAgent.current()[0]
        r,c = self.getAbsRowAndColumn(rCoord)
        print(self.worldArr[r][c])
        if self.worldArr[r][c] == "C":
            for y in range(0,len(self.coins)):
                if r == self.coins[y][0] and c == self.coins[y][1]:
                    self.coins[y][2] = "P"
                    break

    def getAbsRowAndColumn(self,rCoord):
        r = 0
        c = 0
        if self.agentStartingDirection == "anorth":
            r = self.agentStartingPosition[0] + rCoord["Y"]
            c = self.agentStartingPosition[1] + rCoord["X"]
        elif self.agentStartingDirection == "asouth": 
            r = self.agentStartingPosition[0] - rCoord["Y"]
            c = self.agentStartingPosition[1] - rCoord["X"]
        elif self.agentStartingDirection == "aeast": 
            r = self.agentStartingPosition[0] - rCoord["X"]
            c = self.agentStartingPosition[1] + rCoord["Y"]
        elif self.agentStartingDirection == "awest": 
            r = self.agentStartingPosition[0] + rCoord["X"]
            c = self.agentStartingPosition[1] - rCoord["Y"]
        return r,c