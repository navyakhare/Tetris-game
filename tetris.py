import curses
from random import randrange
import level
curses.initscr()
curses.curs_set(0)
win = curses.newwin(18,18,0,0)
win.keypad(1)
win.nodelay(1)

f = [ [0x315,0x4cd,0x13f,0xc47],[0x31d,0x4cf,0x137,0xc45],[0x374,0x374,0x374,0x374],[0x741,0x51c,0xdc3,0xf34],
            [0xfc1,0x73c,0x543,0xd14],[0x311,0x4cc,0x133,0xc44],[0xc34,0x341,0x41c,0x1c3]]
rowfull=0
speed=0

class board():
    def __init__(self,FP,s):
        self.FP=FP
        self.s=s
        
    def putFig(self,FP,s):
        c = lambda el,n: -1 if (n >> el & 3) == 3 else 1 if (n >> el & 3) == 1 else 0
        pos = [ c(i ,f[ FP[3] ][ FP[2] ] ) for i in range(0,15,2)[::-1]]
        return self.chkFig([map(lambda x,y: x+y, FP[0:2]*4,pos)[i-2:i] for i in range(2,9,2)],s)

           
    def chkFig(self,crds,s):
        chk = all([win.inch(c[1],c[0]) & 255 == 32 for c in crds])
        for c in crds: win.addch(c[1],c[0],'X' if s==1 else 32) if ((chk and s == 1) or s == 0) else None
        return True if s == 0 else chk
           
class block(board):
    def __init__(self,FP,key,d,l):
        self.key=key
        self.d=d
        self.FP=FP
        self.l=l
    def MoveFig(self,FP,key,d,l): 
        FP[0] = FP[0] - d if key == curses.KEY_LEFT else FP[0] + d if key == curses.KEY_RIGHT else FP[0]
        FP[1] = FP[1] + d if key in [curses.KEY_DOWN, -1] else FP[1]  
        if key == curses.KEY_UP: FP[2] = 0 if FP[2] + d > 3 else 3 if FP[2] + d < 0 else FP[2] + d
        if l>3:
            FP[1]=2 if key== curses.KEY_BACKSPACE else FP[1]


class gameplay(board,block):
    def __init__(self,score,t):
        self.score=score
        self.t=t
    def chkBoard(self,score,t):
        for i in range(17):
            if all([chr(win.inch(i,x)) == 'X' for x in range(1,17)]):
                rowfull=1
                win.deleteln()
                win.move(1,1)
                win.insertln()
                score=score+90
                win.timeout(t-(score/10))
        return score
    def deleterow(self):
        win.deleteln()
        win.move(1,1)
        win.insertln()
        rowfull=0
    def scoreupdate(self):
        score=score+90
        win.timeout(t-(score/10))
def bar(l):
    if l==4:
        win.addstr(6,2,'XXX')
        win.addstr(4,5,'X')
        win.addstr(9,14,'XX')

    if l==5:
        win.addstr(3,12,'XX')
        win.addstr(6,5,'X')
    


FigPos = [8,3,0,randrange(0,6,1)]


b=board(FigPos,1)
score=b.putFig(FigPos,1)^1
win.timeout(800)
l=1
while 1:
    win.border('|','|','-','-','+','+','+','+')
    l=level.level(score)
    t=level.time(l)
    win.timeout(t)
    bar(l)

    win.addstr(0,8,'Score:'+str(score)+' ')
    win.addstr(0,0,'Level:'+str(l))
    key = win.getch()
    if key == 27: break
    c=block(FigPos,key,1,l)
    c.putFig(FigPos,0)
    c.MoveFig(FigPos,key,1,l)
    if not c.putFig(FigPos,1):
        c.MoveFig(FigPos,key, -1,l)
        c.putFig(FigPos,1)
        if FigPos[1]==3: break
        if key in [curses.KEY_DOWN,-1]:
            a=gameplay(score,t)
            score=score+10
            score = a.chkBoard(score,t)
            if rowfull==1:
                a.deleterow()
                a.scoreupdate()
                
            FigPos = [8,3,0,randrange(0,6,1)]
            c.putFig(FigPos,1)

curses.endwin()
print '\nThanks for playing, your score: '+str(score)+'\n'















