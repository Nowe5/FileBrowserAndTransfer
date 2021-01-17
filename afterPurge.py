class Node:
    def __init__(self, path = self.pwd()):
        self.item = 0 #data
        
        self.dir=path # from pwd
        self.page= 1  #page
        self.position= 1
        self.fileNames=None # ls path | for hidden file -a
        #self.fileInfo=[] #stat -c %A `PATH` | %a parameter for 777
        self.selectedFileInfo=[] #stat -c %A `PATH` | %a parameter for 777
        self.nRef = [None] * len(fileNames)
        self.pRef = None
     
     
     def pwd():
        pass
        #TODO subprocess pwd


class DoublyLinkedList:
    def __init__(self):
        self.startNode = None  # start node ilk oluşturulan node da dursun her zaman
        self.current = None     # current node anlık işlem yaptığımız node da olacak
        
    def insertInEmptyList(self):
        if self.startNode is None:
            newNode = Node()
            self.startNode = newNode
        else:
            print("list is not empty")
            
    def getPrefDir(self): # current path i al son klasörü sil
        pass
        #TODO get parent directory
    
    def getPrefPossition(self):
        pass
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
        newNode.nRef[self.getPrefPossition - 1] = self.current      #   -1 ???
        self.current.pRef = newNode
        self.current = self.current.pRef
        self.current.pRef = self.current        # sola eklediğimiz yeni node'un pref'ini kendine döndürdük.
      
#######################################################################################################
    
    def insert_at_end(self, data):
        if self.startNode is None:
            new_node = Node(data)
            self.startNode = new_node
            return
        n = self.startNode

        while n.nref is not None: # len(n.nref)>0
            n = n.nref
        new_node = Node(data)
        n.nref = new_node
        new_node.pRef = n
        
    def insert_after_item(self, x, data):
        if self.startNode is None:
            print("List is empty")
            return
        else:
            n = self.startNode
            while n is not None:
                if n.item == x:
                    break
                n = n.nref
            if n is None:
                print("item not in the list")
            else:
                new_node = Node(data)
                new_node.pRef = n
                new_node.nref = n.nref
                if n.nref is not None:  # len(n.nref)>0
                    n.nref.prev = new_node
                n.nref = new_node

    def insert_before_item(self, x, data):
        if self.startNode is None:
            print("List is empty")
            return
        else:
            n = self.startNode
            while n is not None:
                if n.item == x:
                    break
                n = n.nref
            if n is None:
                print("item not in the list")
            else:
                new_node = Node(data)
                new_node.nref = n
                new_node.pRef = n.pRef
                if n.pRef is not None:
                    n.pRef.nref = new_node
                n.pRef = new_node

    def delete_at_start(self):
        if self.startNode is None:
            print("The list has no element to delete")
            return 
        if self.startNode.nref is None:
            self.startNode = None
            return
        self.startNode = self.startNode.nref
        self.start_prev = None

    def delete_element_by_value(self, x):
        if self.startNode is None:
            print("The list has no element to delete")
            return 
        if self.startNode.nref is None:
            if self.startNode.item == x:
                self.startNode = None
            else:
                print("Item not found")
            return 

        if self.startNode.item == x:
            self.startNode = self.startNode.nref
            self.startNode.pRef = None
            return

        n = self.startNode
        while n.nref is not None:
            if n.item == x:
                break;
            n = n.nref
        if n.nref is not None:
            n.pRef.nref = n.nref
            n.nref.pRef = n.pRef
        else:
            if n.item == x:
                n.pRef.nref = None
            else:
                print("Element not found")
                
    # def insert_after_item(self, x, data):
    #     if self.startNode is None:
    #         print("List is empty")
    #         return
    #     else:
    #         n = self.startNode
    #         while n is not None:
    #             if n.item == x:
    #                 break
    #             n = n.nref
    #         if n is None:
    #             print("item not in the list")
    #         else:
    #             new_node = Node(data)
    #             new_node.pRef = n
    #             new_node.nref = n.nref
    #             if n.nref is not None:  # len(n.nref)>0
    #                 n.nref.prev = new_node
    #             n.nref = new_node
        
    #    self.startNode = new_node  