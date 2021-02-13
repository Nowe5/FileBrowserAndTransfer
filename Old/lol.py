                
        # while n.nref is not None:
        #     if n == nodeToDelete:
        #         break
        #     n = n.nref
        # if n.nref is not None:
        #     n.pRef.nref = n.nref
        #     n.nref.pRef = n.pRef
        # else:
        #     if n.item == nodeToDelete:
        #         n.pRef.nref = None
        #     else:
        #         print("Element not found")
                
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

        
    # def insertAtEnd(self, data):
    #     if self.startNode is None:
    #         new_node = Node(data)
    #         self.startNode = new_node
    #         return
    #     n = self.startNode

    #     while n.nref is not None: # len(n.nref)>0
    #         n = n.nref
    #     new_node = Node(data)
    #     n.nref = new_node
    #     new_node.pRef = n
        
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

    # def insert_before_item(self, x, data):
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
    #             new_node.nref = n
    #             new_node.pRef = n.pRef
    #             if n.pRef is not None:
    #                 n.pRef.nref = new_node
    #             n.pRef = new_node


    # def delete_at_start(self):
    #     if self.startNode is None:
    #         print("The list has no element to delete")
    #         return 
    #     if self.startNode.nref is None:
    #         self.startNode = None
    #         return
    #     self.startNode = self.startNode.nref
    #     self.start_prev = None