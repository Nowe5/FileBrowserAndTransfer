
import subprocess

class Node:
    def __init__(self, path = self.pwd()):
                
        self.dir=path                   # from pwd
        self.baseName=basename()
        self.page= 1                    #page
        self.position= 1
        self.fileNames=ls()             # ls path | for hidden file -a
        #self.fileInfo=[] #stat -c %A `PATH` | %a parameter for 777
        self.selectedFileInfo=stat()    #stat -c %A `PATH` | %a parameter for 777  #her yukarı aşağı yapıldığında yenilemek gerek
        self.nRef = [None] * len(fileNames)
        self.pRef = None 
   
    def stat(self, path=self.fileNames[self.position-1]):
        output_stat=subprocess.check_output(['stat',"-c","%A", path]).decode('utf-8').strip('\n')
        return [char for char in output_stat] #split stat into characters
        
    def basename(self,path=self.dir):
        output_basename=subprocess.check_output(['basename', path]).decode('utf-8').strip('\n')
        return output_basename

    def pwd(self):
        output_pwd=subprocess.check_output(['pwd']).decode('utf-8').strip('\n')
        return output_pwd

    def ls(self, fullPath=self.dir):
        output_ls=subprocess.check_output(['ls', fullPath]).decode('utf-8')
        return output_ls.splitlines()

class DoublyLinkedList:
    def __init__(self):
        self.startNode = None   # start node ilk oluşturulan node da dursun her zaman
        self.current = None     # current node anlık işlem yaptığımız node da olacak
        self.header = None      # listenin başını işaret ettiğimiz node
        
    def insertInEmptyList(self):
        if self.startNode is None:
            newNode = Node()
            self.startNode = newNode
            self.header = newNode
        else:
            print("list is not empty")
            
    def getPrefDir(self): # current path i al son klasörü sil
        folders = self.current.dir.split('/')
        parentDir="/"
        for word in folders[:-1]:
            parentDir+=word
            
        return parentDir
        #TODO get parent directory

    def getPrefPosition(self):
        pRefDir = self.getPrefDir()
        names = ls(pRefDir)
    
        return names.index(self.current.baseName)
        #pass
        #TODO get parent possition. sola giderken pRef tanımlı olmadığı için pRef pozisyonu bilinmiyor. bilinmediği için insertpRef fonksiyonunda newNode'un nref i atanamıyor. 
    
    def appendNref(self):   # / da iken / eklemek sorun olabilir if le bişeler yap
        newNode = Node(self.current.dir+"/"+self.fileNames[self.position - 1])
        newNode.pRef = self.current
        self.current.nRef[self.position - 1] = newNode
        self.current = newNode
    
    def insertPref(self):
        if self.startNode is None:
            self.insertInEmptyList()
            return
            
        newNode = Node(getParentDir())
        newNode.nRef[self.getPrefPosition] = self.current      #   -1 ???
        self.current.pRef = newNode
        self.current = self.current.pRef
        self.current.pRef = self.current        # sola eklediğimiz yeni node'un pref'ini kendine döndürdük.
        self.header = self.current              # sağa gelip tekrar sola gidince node oluşturursa burası headerın içinden geçebilir
      
    def delete_element_by_value(self, nodeToDelete=self.current):
        if self.startNode is None:
            print("The list has no node to delete")
            return 
        if not self.startNode.nref:
            if self.startNode == nodeToDelete:
                self.startNode = None
            else:
                print("Node not found")
            return 

        # if self.startNode == nodeToDelete:
        #     self.startNode = self.startNode.nref
        #     self.startNode.pRef = None
        #     return
        
        n = self.header

        if not nodeToDelete.dir.startswith(n.dir):
            print("The File has not in Nodes")
            return 
        else:
            searhingList = nodeToDelete.dir[len(n.dir)-1:].split('/')
        
            for file in searhingList:
                if n.nRef.index(file):
                    n = n.nRef[n.nRef.index(file)]
                else: 
                    print("The file not found")
                    break       
                if n.dir == nodeToDelete.dir:
                    n.pRef.nRef[n.pRef.nRef.index(file)]=None
                    n=None
