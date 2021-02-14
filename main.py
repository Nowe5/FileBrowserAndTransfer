from nodeController import Node
from nodeController import DoublyLinkedList
from curses import *
from curses.panel import *
from signal import signal, SIGWINCH

import time

class boxController:
    def __init__(self):

        self.stdscr = initscr()
        self.dList = DoublyLinkedList()

        self.createWindow()
        self.createPanel()
       
        signal(SIGWINCH, self.resizeHandler)

        #TODO:
        # parent, current, child için controller yazılacak.
        # attributes tanımlanır. no-echo highlight vs

    def resizeHandler(self, signum, frame):
        #signal(SIGWINCH, resize_handler) #https://stackoverflow.com/questions/5161552/python-curses-handling-window-terminal-resize
        
        #TODO fullscreen yapınca çalışmıyor
        endwin()
        self.height, self.width = self.stdscr.getmaxyx()
        resizeterm(self.height, self.width)
        self.createWindow()
        self.createPanel()
            
    def createWindow(self):

        self.height, self.width = self.stdscr.getmaxyx()

        #curses.newwin( max_row + 2, maxCol, start_y, start_x  )
        self.parentBox = newwin ( int(self.height*0.93),   int(self.width*0.10),   2, 1 )
        self.currentBox = newwin( int(self.height*0.93),   int(self.width*0.40),   2, int(self.width*0.14) )
        self.childBox = newwin  ( int(self.height*0.93),   int(self.width*0.40),   2, int(self.width*0.57))
        
        self.parentBox.box()
        self.currentBox.box()
        self.childBox.box()

    def createPanel(self):
        self.panelPa = new_panel(self.parentBox)
        self.panelCu = new_panel(self.currentBox)
        self.panelCh = new_panel(self.childBox)

        update_panels()
        doupdate()
        
def main():
    
    #dList = DoublyLinkedList()

    
    box = boxController()
    
    input()
if __name__=="__main__":
    main()

####
        # self.parentBox.addstr(1,1, "This is parent box, over")
        # self.currentBox.addstr(1,1, "This is Current box, over")
        # self.childBox.addstr(1,1, "This is child box, over")
        # update_panels()
        # doupdate()
####
