# PyAgent.py
from pyswip import Prolog

class Agent:
    
    def __init__(self):
        self.prolog = Prolog()
        self.prolog.consult("Quang-Agent.pro")
        #print("PyAgent_Initialize")

    def reborn(self):
        #print("Reborn")
        reborn = list(self.prolog.query("reborn()."))
        #print(reborn)
        # print("PyAgent reborn")

    def reposition(self,L):
        NoQuotesArr = "["
        for i in L:
            NoQuotesArr += i + ","
        NoQuotesArr = NoQuotesArr[:-1]
        NoQuotesArr +="]"
        text = f"reposition({NoQuotesArr})."
        #print(text)
        list(self.prolog.query(text))
        # print("PyAgent reposition")

    def explore(self):
        alist = list(self.prolog.query("explore(L)."))
        # print("PyAgent Explore")
        # print(alist)
        return alist

    def current(self):
        currentCoord = list(self.prolog.query("current(X,Y,D)."))
        #print("PyAgent current")
        #print(currentCoord)
        return currentCoord

    def move(self,A,L):
        NoQuotesArr = "["
        for i in L:
            NoQuotesArr += i + ","
        NoQuotesArr = NoQuotesArr[:-1]
        NoQuotesArr +="]"
        text = f"move({A},{NoQuotesArr})"
        #print(text)
        list(self.prolog.query(text))
        # print("PyAgent move")

    def HasArrow(self):
        self.prolog.query("hasarrow().")
        # print("PyAgent hasarrow")

    def GameOver(self,score):
        print("GameOver: score = " + str(score))
    
    def visited(self):
        visited = list(self.prolog.query("visited(X,Y)."))
        # print("PyAgent visited")
        # print(visited)
        return visited

    def wumpus(self):
        wumpus = list(self.prolog.query("wumpus(X,Y)."))
        # print("PyAgent wumpus")
        # print(wumpus)
        return wumpus

    def confundus(self):
        confundus = list(self.prolog.query("confundus(X,Y)."))
        # print("PyAgent confundus")
        # print(confundus)
        return confundus

    def tingle(self):
        tingle = list(self.prolog.query("tingle(X,Y)."))
        # print("PyAgent tingle")
        # print(tingle)
        return tingle

    def glitter(self):
        glitter = list(self.prolog.query("glitter(X,Y)."))
        # print("PyAgent glitter")
        # print(glitter)
        return glitter

    def stench(self):
        stench = list(self.prolog.query("stench(X,Y)."))
        # print("PyAgent stench")
        # print(stench)
        return stench

    def safe(self):
        safe = list(self.prolog.query("safe(X,Y)."))
        # print("PyAgent safe")
        # print(safe)
        return safe


    def wall(self):
        wall = list(self.prolog.query("wall(X,Y)."))
        # print("PyAgent safe")
        # print(safe)
        return wall
        

    def certainwumpus(self):
        certainwumpus = list(self.prolog.query("certainWumpus(X,Y)."))
        return certainwumpus