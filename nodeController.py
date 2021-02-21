import subprocess
import os.path

class Node:
    def __init__(self, path = None ):
        if path is None:
            path = self.pwd()    
        self.dir=path                   # from pwd
        self.baseName=self.basename()
        self.status = self.stat(self.dir)
        self.position= 1
        self.page= 1                    #page
        self.fileNames=self.ls()             # ls path | for hidden file -a
        self.selectedFileInfo=None
        #self.fileInfo=[] #stat -c %A `PATH` | %a parameter for 777
        
        self.pRef = None
        self.nRef = None
        
        if self.status[0] == "d":
            self.selectedFileInfo=self.stat()    #stat -c %A `PATH` | %a parameter for 777  #her yukarı aşağı yapıldığında yenilemek gerek
            self.nRef = [None] * len(self.fileNames)
        elif self.status[0] == "l" and os.path.isdir( self.readlink(self.dir) ):
            self.selectedFileInfo=self.stat()
            self.nRef = [None] * len(self.fileNames)
    
    def printNode(self):
        print("Directory =",self.dir)
        print("basename = ",self.baseName)
        print("Page num =",self.page)
        print("Position =",self.position)
        print("fileNames =",self.fileNames)
        print("sel file Name =", self.fileNames[self.position-1])
        print("selected file info =",self.selectedFileInfo)
        print("nref =",self.nRef)
        print("pref =",self.pRef)

    #checked
    def stat(self, path=None):
        if path is None:
            path=self.dir+"/"+self.fileNames[self.position-1]
        # elif path is '':
        #     path = '/'
        outputStat=subprocess.check_output(['stat',"-c","%A", path]).decode('utf-8').strip('\n')
        return [char for char in outputStat] #split stat into characters
    
    #checked
    def readlink(self, path=None): #readlink -f /bin/zstdcat
        if path is None:
            path=self.dir+"/"+self.fileNames[self.position-1]
        outputReadlink=subprocess.check_output(['readlink',"-f", path]).decode('utf-8').strip('\n')
        return outputReadlink
    #checked
    def basename(self,path=None):
        if path is None:
            path = self.dir
        outputBasename=subprocess.check_output(['basename', path]).decode('utf-8').strip('\n')
        return outputBasename
    
    #checked
    def pwd(self):
        outputPwd=subprocess.check_output(['pwd']).decode('utf-8').strip('\n')
        return outputPwd
    
    #checked
    def ls(self, fullPath=None):
        if fullPath is None:
            fullPath = self.dir
        outputLs=subprocess.check_output(['ls', fullPath]).decode('utf-8')
        return outputLs.splitlines()

class DoublyLinkedList:
    def __init__(self):
        self.startNode = None   # start node ilk oluşturulan node da dursun her zaman
        self.current = None     # current node anlık işlem yaptığımız node da olacak
        self.header = None      # listenin başını işaret ettiğimiz node
        
        self.insertInEmptyList()
        self.insertPref()
        


        
    
    #checked 
    def insertInEmptyList(self):
        if self.startNode is None:
            newNode = Node()
            self.startNode = newNode
            self.header = newNode
            self.current = newNode
        else:
            return False

    # #checked        
    # def getPrefDir(self): # current path i al son klasörü sil
    #     index = self.current.dir.rfind('/')
    #     parentDir = self.current.dir[:index]
    #     if parentDir.count('/') == 0:
    #          parentDir = '/'
        
    #     return parentDir
    #     #TODO get parent directory

    #checked   
    def getPrefDir(self,path = None):
        if path is None:
            path = self.current.dir
        outputPrefdir= os.path.dirname(path)
        return outputPrefdir

    #checked
    def getPrefPosition(self):
        pRefDir = self.getPrefDir()
        
        names = self.current.ls(pRefDir)
        
        return names.index(self.current.baseName) + 1

        #pass
        #TODO get parent possition. sola giderken pRef tanımlı olmadığı için pRef pozisyonu bilinmiyor. bilinmediği için insertpRef fonksiyonunda newNode'un nref i atanamıyor. 
    
    #checked
    def appendNref(self):   # / da iken / eklemek sorun olabilir if le bişeler yap
  
        slash='/'
        if  self.current.dir == '/':
            slash=''

        
        newNode = Node(self.current.dir+slash+self.current.fileNames[self.current.position - 1])
        newNode.pRef = self.current
        #newNode.printNode()
        self.current.nRef[self.current.position - 1] = newNode
        #self.current.printNode()
        self.current = newNode
       # self.current.printNode()
    
    #checked
    def insertPref(self):
        if self.startNode is None:
            self.insertInEmptyList()
            return

        if self.current.pRef is None and self.current.dir != "/":    
            newNode = Node(self.getPrefDir())
            newNode.nRef[self.getPrefPosition()] = self.current      #   -1 ???
            newNode.position = self.getPrefPosition()#Pref position atandı.
            self.current.pRef = newNode
            #self.current = self.current.pRef
            if self.current.pRef.dir == '/':
                self.current.pRef.pRef = self.current.pRef       # sola eklediğimiz yeni node'un pref'ini kendine döndürdük.
            self.header = self.current              # sağa gelip tekrar sola gidince node oluşturursa burası headerın içinden geçebilir

      
    def delete_element_by_value(self, nodeToDelete=None):

        if nodeToDelete is None:
            nodeToDelete=self.current 
            
        if self.startNode is None:
            #print("The list has no node to delete")
            return False
        if not self.startNode.nRef:
            if self.startNode == nodeToDelete:
                self.startNode = None
            else:
                #print("Node not found")
                return False

        # if self.startNode == nodeToDelete:
        #     self.startNode = self.startNode.nref
        #     self.startNode.pRef = None
        #     return
        
        n = self.header

        if not nodeToDelete.dir.startswith(n.dir):
            #print("The File has not in Nodes")
            return False
        else:
            searhingList = nodeToDelete.dir[len(n.dir)-1:].split('/')
        
            for file in searhingList:
                if n.nRef.index(file):
                    n = n.nRef[n.nRef.index(file)]
                else: 
                    #print("The file not found")
                    break       
                if n.dir == nodeToDelete.dir:
                    n.pRef.nRef[n.pRef.nRef.index(file)]=None
                    #TODO move current node somewhere
                    nodeToDelete = None
