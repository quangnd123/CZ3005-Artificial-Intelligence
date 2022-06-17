:- dynamic([
  visited/2,
  wumpus/2,
  confundus/2,
  tingle/2,
  glitter/2,
  stench/2,
  safe/2,
  current/3,
  hasarrow/0,
  wall/2,
  minX/1,
  maxX/1,
  minY/1,
  maxY/1
]).

reborn:-retractall(visited(_,_)),
retractall(wumpus(_,_)),
retractall(confundus(_,_)),
retractall(tingle(_,_)),
retractall(glitter(_,_)),
retractall(stench(_,_)),
retractall(safe(_,_)),
retractall(current(_,_,_)),
retractall(wall(_,_)),
retractall(hasarrow),
retractall(minX(_)),
retractall(maxX(_)),
retractall(minY(_)),
retractall(maxY(_)),
assert(hasarrow),
assert(current(0,0,rnorth)),
assert(visited(0,0)),
assert(safe(0,0)),
assert(minX(0)),
assert(maxX(0)),
assert(minY(0)),
assert(maxX(0)).

reposition([C,S,T,G,B,SC]):-retractall(visited(_,_)),
retractall(wumpus(_,_)),
retractall(confundus(_,_)),
retractall(tingle(_,_)),
retractall(glitter(_,_)),
retractall(stench(_,_)),
retractall(safe(_,_)),
retractall(current(_,_,_)),
retractall(wall(_,_)),
retractall(minX(_)),
retractall(maxX(_)),
retractall(minY(_)),
retractall(maxY(_)),
assert(current(0,0,rnorth)),
assert(visited(0,0)),
assert(safe(0,0)),
assert(minX(0)),
assert(maxX(0)),
assert(minY(0)),
assert(maxY(0)),
sensory([C,S,T,G,B,SC]).
% map([C,S,T,G,B,SC]).

move(A,L):-(
  (A=moveforward,L=[_,_,_,_,on,_]->sensory(L));
  (action(A),sensory(L))
).
% ,map(L).

action(shoot):- retractall(hasarrow).

action(moveforward):-current(X,Y,D),retractall(current(_,_,_)),(
  (D=rnorth->NewY is Y+1,NewX is X);
  (D=reast->NewX is X+1,NewY is Y);
  (D=rsouth->NewY is Y-1,NewX is X);
  (D=rwest->NewX is X-1,NewY is Y)
),assert(current(NewX,NewY,D)),assert(visited(NewX,NewY)),
minX(MINX),maxX(MAXX),minY(MINY),maxY(MAXY),
(
  (NewX<MINX->retractall(minX(_)),assert(minX(NewX)));
  (NewX>MAXX->retractall(maxX(_)),assert(maxX(NewX)));
  true
),
(
  (NewY<MINY->retractall(minY(_)),assert(minY(NewY)));
  (NewY>MAXY->retractall(maxY(_)),assert(maxY(NewY)));
  true
).

action(turnleft):-current(X,Y,D),retractall(current(_,_,_)),(
  (D=rnorth->NewD = rwest);
  (D=reast->NewD = rnorth);
  (D=rsouth->NewD = reast);
  (D=rwest->NewD = rsouth)
),assert(current(X,Y,NewD)).

action(turnright):-current(X,Y,D),retractall(current(_,_,_)),(
  (D=rnorth->NewD = reast);
  (D=reast->NewD = rsouth);
  (D=rsouth->NewD = rwest);
  (D=rwest->NewD = rnorth)
),assert(current(X,Y,NewD)).

action(pickup):-current(X,Y,_),retractall(glitter(X,Y)).

% sensory([on,S,T,G,B,SC]):-reposition([on,S,T,G,B,SC]).

same([X1,Y1],[X2,Y2]):-X1=:=X2,Y1=:=Y2.
adj([X,Y],[A,B]):- 
  (A is X+1,B is Y);(A is X-1,B is Y);
  (A is X,B is Y+1);(A is X,B is Y-1).
count_stench(Count,SortedList):-
  findall([X,Y], stench(X,Y), List),sort(List,SortedList),
  length(SortedList, Count).
count_wumpus(Count):-
  findall([X,Y], (wumpus(X,Y),\+safe(X,Y),\+wall(X,Y)), List),sort(List,SortedList),
  length(SortedList, Count).
update_wumpus([],_).
update_wumpus([[A,B]|Rest],L):-
  (
    not_member([A,B],L),\+confundus(A,B)->assert(safe(A,B)),retractall(wumpus(A,B));
    not_member([A,B],L),confundus(A,B)->retractall(wumpus(A,B));
    true
  ),update_wumpus(Rest,L).

sensory([_,S,T,G,B,SC]):-current(X,Y,D),
  (
    (count_wumpus(Count_wumpus),Count_wumpus=:=1,S=on->assert(stench(X,Y)));
    ((
      S=on->assert(stench(X,Y)),
      (
        Y1 is Y+1,\+safe(X,Y1),\+wall(X,Y1), assert(wumpus(X,Y1));
        true
      )
      ,
      (
        Y2 is Y-1,\+safe(X,Y2),\+wall(X,Y2), assert(wumpus(X,Y2));
        true
      )
      ,
      (
      X1 is X+1,\+safe(X1,Y),\+wall(X1,Y), assert(wumpus(X1,Y));
      true
      )
      ,
      (
      X2 is X-1,\+safe(X2,Y),\+wall(X2,Y), assert(wumpus(X2,Y));
      true
      )
      ,
      count_stench(C,L),(
        (
          C=:=1->true
        );
        (
          C=:=2->L=[[X3,Y3],[X4,Y4]],
          findall([E,F],(adj([X3,Y3],[E,F]),adj([X4,Y4],[E,F])),
          List),
          findall([H,K],(wumpus(H,K)),WumpusList),
          update_wumpus(WumpusList,List)
        );
        (
          L=[[X3,Y3],[X4,Y4],[X5,Y5]|_],
          findall([E,F],(adj([X3,Y3],[E,F]),adj([X4,Y4],[E,F]),adj([X5,Y5],[E,F])),
          List),
          findall([H,K],(wumpus(H,K)),WumpusList),
          update_wumpus(WumpusList,List)
        )
      )
    );
    S=off->true)
  ),
  (
    (
      T=on->assert(tingle(X,Y)),
      (
        Y1 is Y+1,\+safe(X,Y1),\+wall(X,Y1), assert(confundus(X,Y1));
        true
      )
      ,
      (
        Y2 is Y-1,\+safe(X,Y2),\+wall(X,Y2), assert(confundus(X,Y2));
        true
      )
      ,
      (
      X1 is X+1,\+safe(X1,Y),\+wall(X1,Y), assert(confundus(X1,Y));
      true
      )
      ,
      (
      X2 is X-1,\+safe(X2,Y),\+wall(X2,Y), assert(confundus(X2,Y));
      true
      )
    );
    T=off->true
  ),
  (
    G=on->assert(glitter(X,Y));
    G=off->true
  ),
  (
    B=on,D=rnorth->Y1 is Y+1,assert(wall(X,Y1)),retractall(wumpus(X,Y1)),retractall(confundus(X,Y1));
    B=on,D=reast->X1 is X+1, assert(wall(X1,Y)),retractall(wumpus(X1,Y)),retractall(confundus(X1,Y));
    B=on,D=rsouth->Y2 is Y-1, assert(wall(X,Y2)),retractall(wumpus(X,Y2)),retractall(confundus(X,Y2));
    B=on,D=rwest->X2 is X-1, assert(wall(X2,Y)),retractall(wumpus(X2,Y)),retractall(confundus(X2,Y));
    B=off->true
  ),
  (
    SC=on->retractall(wumpus(_,_)), retractall(stench(_,_));
    SC=off->true
  ),
  (
    (
      S=off,T=off->
      Y1 is Y+1, asserta(safe(X,Y1)),retractall(wumpus(X,Y1)),retractall(confundus(X,Y1)),
      Y2 is Y-1, asserta(safe(X,Y2)),retractall(wumpus(X,Y2)),retractall(confundus(X,Y2)),
      X1 is X+1, asserta(safe(X1,Y)),retractall(wumpus(X1,Y)),retractall(confundus(X1,Y)),
      X2 is X-1, asserta(safe(X2,Y)),retractall(wumpus(X2,Y)),retractall(confundus(X2,Y))
    );
    true
  ).

map(L):-write('Relative map:'),nl,current(X,Y,_),minX(MINX),maxX(MAXX),minY(MINY),maxY(MAXY),
(
  X-MINX>=MAXX-X -> DX is X-MINX;
  X-MINX<MAXX-X  -> DX is MAXX-X
),
(
  Y-MINY>=MAXY-Y -> DY is Y-MINY;
  Y-MINY<MAXY-Y  -> DY is MAXY-Y
),
StartX is 0, EndX is (DX+1)*6+3, StartY is 0, EndY is (DY+1)*6+3,
loopRows(StartX,EndX,StartY,EndY,L).

loopRows(StartX,EndX,StartY,EndY,L):-
  (
    StartY=\=EndY -> loopCols(StartX,EndX,StartY,EndY,L),nl,
    NewStartY is StartY+1,loopRows(StartX,EndX,NewStartY,EndY,L)
  );
  StartY=:=EndY->true.

loopCols(StartX,EndX,StartY,EndY,L):-
  (
    StartX=\=EndX,element(StartX,EndX,StartY,EndY,L),write(' '),
    NewStartX is StartX+1, loopCols(NewStartX,EndX,StartY,EndY,L)
  );
  StartX=:=EndX->true.

element(StartX,EndX,StartY,EndY,L):-current(CurX,CurY,D),
CellX is StartX//3+CurX-EndX//6,CellY is EndY//6-StartY//3+CurY,
RelativeX is mod(StartX,3), RelativeY is mod(StartY,3),
(wall(CellX,CellY)->write('#');
(
  (
    RelativeY=:=0,RelativeX=:=0,
    ( 
      \+safe(CellX,CellY),CellX=:=CurX,CellY=:=CurY,L=[on,_,_,_,_,_]->write('%');
      write('.')
    )
  );
  (
    RelativeY=:=0,RelativeX=:=1,
    (
      CellX=:=CurX,CellY=:=CurY,L=[_,on,_,_,_,_]->write('=');
      write('.')
    )
  );
  (
    RelativeY=:=0,RelativeX=:=2,
    (
      CellX=:=CurX,CellY=:=CurY,L=[_,_,on,_,_,_]->write('T');
      write('.')
    )
  );
  (
    RelativeY=:=1,RelativeX=:=0,
    (
      CellX=:=CurX,CellY=:=CurY->write('-');
      glitter(CellX,CellY)->write('-');
      \+safe(CellX,CellY),confundus(CellX,CellY)->write('-');
      \+safe(CellX,CellY),wumpus(CellX,CellY)->write('-');
      write(' ')
    )
  );
  (
    RelativeY=:=1,RelativeX=:=1,
    (
      CellX=:=CurX,CellY=:=CurY,D=rnorth->write('^');
      CellX=:=CurX,CellY=:=CurY,D=reast->write('>');
      CellX=:=CurX,CellY=:=CurY,D=rwest->write('<');
      CellX=:=CurX,CellY=:=CurY,D=rsouth->write('v');
      safe(CellX,CellY),visited(CellX,CellY)->write('S');
      safe(CellX,CellY)->write('s');
      \+safe(CellX,CellY),confundus(CellX,CellY),wumpus(CellX,CellY)->write('U');
      \+safe(CellX,CellY),confundus(CellX,CellY)->write('O');
      \+safe(CellX,CellY),wumpus(CellX,CellY)->write('W');
      write('?')
    )
  );
  (
    RelativeY=:=1,RelativeX=:=2,
    (
      CellX=:=CurX,CellY=:=CurY->write('-');
      glitter(CellX,CellY)->write('-');
      \+safe(CellX,CellY),confundus(CellX,CellY)->write('-');
      \+safe(CellX,CellY),wumpus(CellX,CellY)->write('-');
      write(' ')
    )
  );
  (
    RelativeY=:=2,RelativeX=:=0,
    (
      CellX=:=CurX,CellY=:=CurY,L=[_,_,_,on,_,_]->write('*');
      write('.')
    )
  );
  (
    RelativeY=:=2,RelativeX=:=1,
    (
      CellX=:=CurX,CellY=:=CurY,L=[_,_,_,_,on,_]->write('B');
      write('.')
    )
  );
  (
    RelativeY=:=2,RelativeX=:=2,
    (
      CellX=:=CurX,CellY=:=CurY,L=[_,_,_,_,_,on]->write('@');
      write('.')
    )
  )
)).

explore(L):-current(X,Y,D),
(
  (
    breadth_first([X,Y,D],_,L);
    L=[]
  )
).

breadth_first([StartX,StartY,StartD], Path,L):-
  bfs([[[StartX,StartY,StartD]]],[[]], Path,L).


bfs( [Visited|Rest],[ActionList|ActionRest], Path,L) :-
  Visited = [[StartX,StartY,StartD]|_], 
  (
    (
      \+visited(StartX,StartY)->L= ActionList
    );           
    (
      (
        (
          X1 is StartX+1,Y1 is StartY,not_member([X1,Y1],Visited),
          (
            safe(X1,Y1),\+wall(X1,Y1)->navigate([StartX,StartY,StartD],[X1,Y1,D1],NewAction1)
            ; wumpus(X1,Y1),count_wumpus(Count),Count=:=1->navigate_and_kill([StartX,StartY,StartD],[X1,Y1,D1],NewAction1)
          )
          -> append([[X1,Y1,D1]],Visited,VisitedExtended1),
          append( Rest, [VisitedExtended1], UpdatedQueue1),
          append(ActionList,NewAction1,ActionListExtended1),
          append( ActionRest, [ActionListExtended1], UpdatedActionQueue1)
        );
        (
          append( Rest, [], UpdatedQueue1),
          append(ActionRest, [],UpdatedActionQueue1)
        )
      ),
      (
        (
            X2 is StartX-1,Y2 is StartY,not_member([X2,Y2],Visited),
            (
              safe(X2,Y2),\+wall(X2,Y2)->navigate([StartX,StartY,StartD],[X2,Y2,D2],NewAction2)
              ;wumpus(X2,Y2),count_wumpus(Count),Count=:=1->navigate_and_kill([StartX,StartY,StartD],[X2,Y2,D2],NewAction2)
            )
            -> append([[X2,Y2,D2]],Visited,VisitedExtended2),
            append( UpdatedQueue1, [VisitedExtended2], UpdatedQueue2),
            append(ActionList,NewAction2,ActionListExtended2),
            append( UpdatedActionQueue1, [ActionListExtended2], UpdatedActionQueue2)
        );
        (
            append( UpdatedQueue1, [], UpdatedQueue2),
            append(UpdatedActionQueue1, [],UpdatedActionQueue2)
        )
      ),
      (
          (
              X3 is StartX,Y3 is StartY+1,not_member([X3,Y3],Visited),
              (
                safe(X3,Y3),\+wall(X3,Y3)->navigate([StartX,StartY,StartD],[X3,Y3,D3],NewAction3)
                ;wumpus(X3,Y3),count_wumpus(Count),Count=:=1->navigate_and_kill([StartX,StartY,StartD],[X3,Y3,D3],NewAction3)
              )
    
              -> append([[X3,Y3,D3]],Visited,VisitedExtended3),
              append( UpdatedQueue2, [VisitedExtended3], UpdatedQueue3),
              append(ActionList,NewAction3,ActionListExtended3),
              append( UpdatedActionQueue2, [ActionListExtended3], UpdatedActionQueue3)
          );
          (
              append( UpdatedQueue2, [], UpdatedQueue3),
              append(UpdatedActionQueue2, [],UpdatedActionQueue3)
          )
          
      ),
      (
        (
            X4 is StartX,Y4 is StartY-1,not_member([X4,Y4],Visited),
            (
              safe(X4,Y4),\+wall(X4,Y4)->navigate([StartX,StartY,StartD],[X4,Y4,D4],NewAction4)
              ;wumpus(X4,Y4),count_wumpus(Count),Count=:=1->navigate_and_kill([StartX,StartY,StartD],[X4,Y4,D4],NewAction4)
            )
            
            -> append([[X4,Y4,D4]],Visited,VisitedExtended4),
            append( UpdatedQueue3, [VisitedExtended4], UpdatedQueue4),
            append(ActionList,NewAction4,ActionListExtended4),
            append( UpdatedActionQueue3, [ActionListExtended4], UpdatedActionQueue4)
        );
        (
            append( UpdatedQueue3, [], UpdatedQueue4),
            append(UpdatedActionQueue3, [],UpdatedActionQueue4)
        )
      ),
      bfs( UpdatedQueue4,UpdatedActionQueue4, Path ,L)
    )
  ).

navigate([CurX,CurY,D],[NewX,NewY,NewD],NewAction):-
  NewY-CurY=:=1,D=rnorth->NewD=rnorth,NewAction=[moveforward];
  NewY-CurY=:=1,D=reast->NewD=rnorth,NewAction=[turnleft,moveforward];
  NewY-CurY=:=1,D=rwest->NewD=rnorth,NewAction=[turnright,moveforward];
  NewY-CurY=:=1,D=rsouth->NewD=rnorth,NewAction=[turnright,turnright,moveforward];
  CurY-NewY=:=1,D=rnorth->NewD=rsouth,NewAction=[turnright,turnright,moveforward];
  CurY-NewY=:=1,D=reast->NewD=rsouth,NewAction=[turnright,moveforward];
  CurY-NewY=:=1,D=rwest->NewD=rsouth,NewAction=[turnleft,moveforward];
  CurY-NewY=:=1,D=rsouth->NewD=rsouth,NewAction=[moveforward];
  NewX-CurX=:=1,D=rnorth->NewD=reast,NewAction=[turnright,moveforward];
  NewX-CurX=:=1,D=reast->NewD=reast,NewAction=[moveforward];
  NewX-CurX=:=1,D=rwest->NewD=reast,NewAction=[turnright,turnright,moveforward];
  NewX-CurX=:=1,D=rsouth->NewD=reast,NewAction=[turnleft,moveforward];
  CurX-NewX=:=1,D=rnorth->NewD=rwest,NewAction=[turnleft,moveforward];
  CurX-NewX=:=1,D=reast->NewD=rwest,NewAction=[turnright,turnright,moveforward];
  CurX-NewX=:=1,D=rwest->NewD=rwest,NewAction=[moveforward];
  CurX-NewX=:=1,D=rsouth->NewD=rwest,NewAction=[turnright,moveforward].

navigate_and_kill([CurX,CurY,D],[NewX,NewY,NewD],NewAction):-
  NewY-CurY=:=1,D=rnorth->NewD=rnorth,NewAction=[shoot,moveforward];
  NewY-CurY=:=1,D=reast->NewD=rnorth,NewAction=[turnleft,shoot,moveforward];
  NewY-CurY=:=1,D=rwest->NewD=rnorth,NewAction=[turnright,shoot,moveforward];
  NewY-CurY=:=1,D=rsouth->NewD=rnorth,NewAction=[turnright,turnright,shoot,moveforward];
  CurY-NewY=:=1,D=rnorth->NewD=rsouth,NewAction=[turnright,turnright,shoot,moveforward];
  CurY-NewY=:=1,D=reast->NewD=rsouth,NewAction=[turnright,shoot,moveforward];
  CurY-NewY=:=1,D=rwest->NewD=rsouth,NewAction=[turnleft,shoot,moveforward];
  CurY-NewY=:=1,D=rsouth->NewD=rsouth,NewAction=[shoot,moveforward];
  NewX-CurX=:=1,D=rnorth->NewD=reast,NewAction=[turnright,shoot,moveforward];
  NewX-CurX=:=1,D=reast->NewD=reast,NewAction=[shoot,moveforward];
  NewX-CurX=:=1,D=rwest->NewD=reast,NewAction=[turnright,turnright,shoot,moveforward];
  NewX-CurX=:=1,D=rsouth->NewD=reast,NewAction=[turnleft,shoot,moveforward];
  CurX-NewX=:=1,D=rnorth->NewD=rwest,NewAction=[turnleft,shoot,moveforward];
  CurX-NewX=:=1,D=reast->NewD=rwest,NewAction=[turnright,turnright,shoot,moveforward];
  CurX-NewX=:=1,D=rwest->NewD=rwest,NewAction=[shoot,moveforward];
  CurX-NewX=:=1,D=rsouth->NewD=rwest,NewAction=[turnright,shoot,moveforward].

not_member(_, []).
not_member([X,Y], [[U,V,_]|Ys]) :-X=U,Y=V -> fail; not_member([X,Y], Ys).
not_member([X,Y], [[U,V]|Ys]) :-X=U,Y=V -> fail; not_member([X,Y], Ys).