from nodeController import Node
from nodeController import DoublyLinkedList

def main():
    
    dList = DoublyLinkedList()

    dList.insertPref()

    #dList.appendNref()

    dList.insertPref()
    
    dList.insertPref()

    dList.insertPref()
    dList.insertPref()
    dList.insertPref()

    dList.current.position = 6
    
    dList.appendNref()
    dList.appendNref()

if __name__=="__main__":
    main()