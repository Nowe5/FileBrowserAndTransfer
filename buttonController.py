import curses

class buttonController:
    def __init__(self,box):
        self.KEY_EXIT = ord('q')
        self.box = box
        self.KEY = box.stdscr.getch()
        self.stdscr = box.stdscr        
        
               
        self.getKey()


    def getKey(self):
        KEY = self.KEY
        while KEY is not self.KEY_EXIT:
            
            if KEY == curses.KEY_DOWN:
                self.KEY_DOWN_PRESSED()

            elif KEY == curses.KEY_UP:
                self.KEY_UP_PRESSED()

            elif KEY == curses.KEY_LEFT:
                self.KEY_LEFT_PRESSED()

            elif KEY == curses.KEY_RIGHT:
                self.KEY_RIGHT_PRESSED()
            
            KEY = self.stdscr.getch()
            
    def KEY_DOWN_PRESSED(self):
        if  self.box.dList.current.position < len( self.box.dList.current.fileNames):
            self.box.dList.current.position += 1
            self.box.dList.current.selectedFileInfo =  self.box.dList.current.stat()
            self.box.updateCurrent()
            self.box.updateChild()

    def KEY_UP_PRESSED(self):
        if  self.box.dList.current.position > 1:
            self.box.dList.current.position -= 1
            self.box.dList.current.selectedFileInfo =  self.box.dList.current.stat()
            self.box.updateCurrent()
            self.box.updateChild()


    def KEY_LEFT_PRESSED(self):
        self.box.dList.current = self.box.dList.current.pRef
        # self.box.dList.current =  self.box.dList.current.pRef
        self.box.dList.insertPref()

        self.box.rowNum = len( self.box.dList.current.fileNames)

        if self.box.dList.current.dir == "/":
            self.box.panelPa.hide()
        else:
            if self.box.panelPa.hidden():
                self.box.panelPa.show()
            self.box.updateParent()

        self.box.updateCurrent()
        self.box.updateChild()

    def KEY_RIGHT_PRESSED(self):
        if  self.box.dList.current.nRef[ self.box.dList.current.position - 1] is None:
            self.box.dList.appendNref()
        else:
            self.box.dList.current = self.box.dList.current.nRef[ self.box.dList.current.position - 1]
        
        self.box.rowNum = len(self.box.dList.current.fileNames)   
        self.box.updateParent()
        self.box.updateCurrent()
        self.box.updateChild()

