from curses import *
from nodeController import Node
from nodeController import DoublyLinkedList
from buttonController import buttonController
from curses.panel import *
from signal import signal, SIGWINCH
import os
from math import ceil

import time

class boxController:
    def __init__(self):

        self.stdscr = initscr()
        self.height, self.width = self.stdscr.getmaxyx()

        self.dList = DoublyLinkedList()
        self.maxRow = int(self.height*0.93)
        self.rowNum = len(self.dList.current.fileNames)
        self.rowNumPref = len(self.dList.current.pRef.fileNames)

        self.dList.current.page = ceil(self.dList.current.position / self.maxRow)
        self.dList.current.pRef.page = ceil(self.dList.current.pRef.position / self.maxRow)
        
        
        
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
    
    
    def selectPagePosDOWN(self,flag = None):
        if flag == 0 or flag == None:
            self.updatePageNPosDOWN(self.dList.current, self.rowNum)
        elif flag == 1:
            self.updatePageNPosDOWN(self.dList.current.pRef, self.rowNumPref)
    
    def updatePageNPosDOWN(self, node, rowNum):
        
        pages = int( ceil( rowNum / self.maxRow ) )
    
        node.page = int(node.position / self.maxRow)

    
        if node.page == 1:
            if node.position < self.maxRow:
                node.position += 1
            elif pages > 1:
                node.position += 1
                node.page += 1
                #position = 1 + ( maxRow * ( page - 1 ) )
        
        
        elif node.page == pages:
            if node.position < rowNum:
                node.position = node.position + 1
        
        
        elif node.position < self.maxRow + ( self.maxRow * ( node.page - 1 ) ):
                    node.position += 1
       
       
        else:
            node.position += 1
            node.page += 1
            #position = 1 + ( maxRow * ( node.page - 1 ) )

    def selectPagePosUP(self,flag = None):
        if flag == 0 or flag == None:
            self.updatePageNPosUP(self.dList.current, self.rowNum)
        elif flag == 1:
            self.updatePageNPosUP(self.dList.current.pRef, self.rowNumPref)
    
    def updatePageNPosUP(self, node, rowNum):
        
        #pages = int( ceil( rowNum / self.maxRow ) )
    
        node.page = int(node.position / self.maxRow)

        if node.page == 1:
            if node.position > 1:
                node.position = node.position - 1


                
        elif node.position > ( 1 + ( self.maxRow * ( node.page - 1 ) ) ):
            node.position = node.position - 1
        else:
            node.page = node.page - 1
            node.position = self.maxRow + ( self.maxRow * ( node.page - 1 ) )
    
    
    def updateCurrent(self):
        self.currentBox.erase()

        current = self.dList.current
        currentMaxRow = int( self.maxRow * ( current.page - 1 ) )
        
        for i in range(1 + currentMaxRow, 1 +self.maxRow + currentMaxRow):
            if self.rowNum == 0:
                    self.currentBox.addstr( 1, 1, "There aren't strings",  self.highlightText )
            else:
                if ( i + ( self.maxRow * ( current.page - 1 ) ) == current.position + ( self.maxRow * ( current.page - 1 ) ) ):
                    self.currentBox.addstr( i - ( self.maxRow  * ( current.page - 1 ) ), 2, current.fileNames[ i - 1 ], self.highlightText )
                else:
                    self.currentBox.addstr( i - ( self.maxRow  * ( current.page - 1 ) ), 2,  current.fileNames[ i - 1 ], self.normalText )
                if i == self.rowNum:
                    break
        

        self.currentBox.refresh()

        
    def updateParent(self):
        if not self.dList.current.dir == "/":
            self.parentBox.erase()
            
            parent = self.dList.current.pRef
            currentMaxRow = ( self.maxRow * ( parent.page - 1 ) )
            
            for i in range(1 + currentMaxRow, 1 + self.maxRow + currentMaxRow):
                if self.rowNumPref == 0:
                        self.parentBox.addstr( 1, 1, "There aren't strings",  self.highlightText )
                else:
                    if ( i + ( self.maxRow * ( parent.page - 1 ) ) == parent.position + ( self.maxRow * ( parent.page - 1 ) ) ):
                        self.parentBox.addstr( i - ( self.maxRow  * ( parent.page - 1 ) ), 2, parent.fileNames[ i - 1 ], self.highlightText )
                    else:
                        self.parentBox.addstr( i - ( self.maxRow  * ( parent.page - 1 ) ), 2,  parent.fileNames[ i - 1 ], self.normalText )
                    if i == self.rowNumPref:
                        break
        

            self.parentBox.refresh()


    def updateChild(self):
        self.childBox.erase()
        current = self.dList.current
        childFileName = current.fileNames[current.position-1]
        
        if current.selectedFileInfo[0] == "d" or (current.selectedFileInfo[0] == "l" and os.path.isdir( current.readlink(current.dir+"/"+childFileName) )): # iki slash nanay mı ??
            fileNames = current.ls(current.dir + "/" +childFileName)
            if current.nRef[current.position-1] is None:
                position = 1
                page = 1
                currentMaxRow = 0
            else:
                position = current.nRef[current.position-1].position
                page = current.nRef[current.position-1].page
                currentMaxRow = ( self.maxRow * ( current.nRef[current.position-1].page - 1 ) )
            rowNum = len(fileNames)
            
     
            for i in range(1 + currentMaxRow, 1 +self.maxRow + currentMaxRow):
                if rowNum == 0:
                        self.childBox.addstr( 1, 1, "There aren't strings",  self.highlightText )
                else:
                    if ( i + ( self.maxRow * ( page - 1 ) ) == position + ( self.maxRow * ( page - 1 ) ) ):
                        self.childBox.addstr( i - ( self.maxRow  * ( page - 1 ) ), 2, fileNames[ i - 1 ], self.highlightText )
                    else:
                        self.childBox.addstr( i - ( self.maxRow  * ( page - 1 ) ), 2,  fileNames[ i - 1 ], self.normalText )
                    if i == rowNum:
                        break

        
        else:
            self.childBox.addstr( 2, 2, "Not a Directory",  self.highlightText )
        

        self.childBox.refresh()
        

def main():
       
    box = boxController()
    button = buttonController(box)
    
if __name__=="__main__":
    main()
