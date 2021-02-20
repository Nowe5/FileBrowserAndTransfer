from curses import *
from nodeController import Node
from nodeController import DoublyLinkedList
from buttonController import buttonController
from curses.panel import *
from signal import signal, SIGWINCH
import os

import time

class boxController:
    def __init__(self):

        self.stdscr = initscr()
        self.height, self.width = self.stdscr.getmaxyx()
        self.dList = DoublyLinkedList()
        self.maxRow = int(self.height*0.93)
        self.rowNum = len(self.dList.current.fileNames)
        curs_set(0)#curserı gizle
        noecho()# yazdığın şeyi gizliyo
        cbreak() #enter a basmadan girdi ile etkileşim için
        self.stdscr.keypad(True) # özel tuşları algılama. page up page down vs
        beep() #beep çalışmayı
        start_color() 
        init_pair(1, COLOR_CYAN, COLOR_BLUE)
        init_pair(2, COLOR_BLACK, COLOR_BLUE)
        init_pair(3, COLOR_BLACK, COLOR_GREEN)
        self.highlightText  = color_pair( 2 )
        self.normalText     = A_NORMAL
       
        self.createWindow()
        self.createPanel()

        
        signal(SIGWINCH, self.resizeHandler)

        self.updateCurrent()
        self.updateParent()
        self.updateChild()
        #boxChild.addstr( 1, 1, "Cannot Access", highlightText )

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
        #self.createPanel()
        #TODO: maxRow ve maxCol u updatele
            
    def createWindow(self):

        self.height, self.width = self.stdscr.getmaxyx()

        #curses.newwin( max_row + 2, maxCol, start_y, start_x  )
        self.parentBox  = newwin    ( self.maxRow,   int(self.width*0.15),   2, 1 )
        self.currentBox = newwin    ( self.maxRow,   int(self.width*0.40),   2, int(self.width*0.17))
        self.childBox   = newwin    ( self.maxRow,   int(self.width*0.40),   2, int(self.width*0.57))
        
        self.parentBox.addstr(1,1, "This is parent box, over", A_REVERSE)

        self.parentBox.box()
        self.currentBox.box()
        self.childBox.box()
        self.parentBox.border(" "," "," "," ") #borderlara hangi karakter koyulacağı. köşeler için 4 tane daha ekenebiliyor
        self.currentBox.border(" "," "," "," ")
        self.childBox.border(" "," "," "," ")

    def createPanel(self):
        self.panelPa = new_panel(self.parentBox)
        self.panelCu = new_panel(self.currentBox)
        self.panelCh = new_panel(self.childBox)

        update_panels()
        doupdate()
    
    def updateCurrent(self):
        self.currentBox.erase()

        current = self.dList.current

        for i in range(self.rowNum):
            if i == current.position-1:
                self.currentBox.addstr( i+2, 2, current.fileNames[i],  self.highlightText )
            else:
                self.currentBox.addstr( i+2, 2, current.fileNames[i],  self.normalText )

        self.currentBox.refresh()

        # for i in range( 1, self.maxRow  + 1 ):
        #     if rowNum == 0:
        #         boxParent.addstr( 1, 1, "There aren't strings", highlightText )
        #     else:
        #         if self.dList.current.fileNames[i -1] == pwd().split('/')[-1]: #l
        #             boxParent.addstr( i, 2, str( i ) + " - " + self.dList.current.fileNames[ i - 1 ], highlightText )
        #             #boxParent.addstr( i, 2, str( i ) + " - " + pwd().split('/')[-1], highlightText )
        #             self.dList.current.position=i
        #         else:
        #             boxParent.addstr( i, 2, str( i ) + " - " + self.dList.current.fileNames[ i - 1 ], normalText )
        #     if i == row_num:
        #         break 

    def updateParent(self):
        if not self.dList.current.dir == "/":
            self.parentBox.erase()
            parent = self.dList.current.pRef

            for i in range(len(parent.fileNames)):
                if i == parent.position-1:
                    self.parentBox.addstr( i+2, 2, parent.fileNames[i],  self.highlightText )
                else:
                    self.parentBox.addstr( i+2, 2, parent.fileNames[i],  self.normalText )

            self.parentBox.refresh()


    def updateChild(self):
        self.childBox.erase()
        current = self.dList.current
        childFileName = current.fileNames[current.position-1]
        
        if current.selectedFileInfo[0] == "d" or (current.selectedFileInfo[0] == "l" and os.path.isdir( current.readlink(current.dir+"/"+childFileName) )): # iki slash nanay mı ??
            fileNames = current.ls(current.dir + "/" +childFileName)
            if current.nRef[current.position-1] is None:
                position = 1
            else:
                position = current.nRef[current.position-1].position

            for i in range(len(fileNames)):
                if i == position - 1:
                    self.childBox.addstr( i+2, 2, fileNames[i],  self.highlightText )
                else:
                    self.childBox.addstr( i+2, 2, fileNames[i],  self.normalText )
        
        
        
        else:
            self.childBox.addstr( 2, 2, "Not a Directory",  self.highlightText )
        

        self.childBox.refresh()
        

def main():
       
    box = boxController()
    button = buttonController(box)
    
if __name__=="__main__":
    main()
