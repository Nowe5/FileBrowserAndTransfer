import sys, os
import curses
import subprocess
from math import *
import socket

def pwd():
    firstPwd = subprocess.check_output(['pwd']).decode('utf-8').strip('\n')
    return firstPwd

def lsP(path):
    
    output_ls=subprocess.check_output(['ls', path+"/.."]).decode('utf-8')
    return output_ls.splitlines()

def ls(path):
    
    output_ls=subprocess.check_output(['ls', path]).decode('utf-8')
    return output_ls.splitlines()

""" def ls():
    
    output_ls=subprocess.check_output(['ls']).decode('utf-8')
    return output_ls.splitlines()
     """


def refreshChild(boxChild,ourPwd,stdscr,selectedDir): #if os.path.isdir(path):
    boxChild.erase()
    
    height, width = stdscr.getmaxyx()
    start_x = int((width // 2))
    start_y = int((height // 2) - 2)
    maxCol=width // 3-3
    max_row = height-5 #max number of rows

    highlightText = curses.color_pair( 2 )
    normalText = curses.A_NORMAL

    childPwd='/'
    # / değilse / koy
    if ourPwd is "/":
        childPwd = ourPwd + selectedDir 
        
    else:
        childPwd = ourPwd +"/"+selectedDir
    #todo: Detaylı şekilde olacak.
    if  os.path.isfile(childPwd) or not os.access(childPwd, os.X_OK):
        boxChild.addstr( 1, 1, "Cannot Access", highlightText )
        boxChild.border( 0 )
        stdscr.refresh()
        boxChild.refresh()
        return -1
    strings = ls(childPwd)
    row_num = len( strings )
    position = 1
    

    for i in range( 1, max_row  + 1 ):
        if row_num == 0:
            boxChild.addstr( 1, 1, "No Files or Dirs inside", highlightText )
        else:
            if (i == position):
                boxChild.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
            else:
                boxChild.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], normalText )
            if i == row_num:
                break
    
    boxChild.border( 0 )
    stdscr.refresh()
    boxChild.refresh()
    return position


def refreshParent(boxParent,ourPwd,stdscr):
    boxParent.erase()
    height, width = stdscr.getmaxyx()

    start_x = int((width // 2))
    start_y = int((height // 2) - 2)
    maxCol=width // 3-3
    max_row = height-5 #max number of rows

    strings = lsP( ourPwd )
    row_num = len( strings )
    position = 0

    highlightText = curses.color_pair( 2 )
    normalText = curses.A_NORMAL

    for i in range( 1, max_row  + 1 ):
        if row_num == 0:
            boxParent.addstr( 1, 1, "There aren't strings", highlightText )
        else:
            if strings[i -1] == ourPwd.split('/')[-1]: #l
                #boxParent.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
                boxParent.addstr( i, 2, str( i ) + " - " + ourPwd.split('/')[-1], highlightText )
                position = i
            else:
                boxParent.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], normalText )
            #boxParent.addstr( 20, 2, str( 61 ) + " - " + ourPwd.split('/')[-1], highlightText )
            if i == row_num:
                break
    
    boxParent.border( 0 )
    stdscr.refresh()
    boxParent.refresh()
    return position


def drawChild(stdscr, selectedDir): #if os.path.isdir(path):

    height, width = stdscr.getmaxyx()

    start_x = int((width))
    start_y = int((height // 2) - 2)
    maxCol=width // 3-3
    max_row = height-5 #max number of rows
    boxChild = curses.newwin( max_row + 2, maxCol, 1, start_x - maxCol-2 )
    boxChild.box()

    highlightText = curses.color_pair( 2 )
    normalText = curses.A_NORMAL
    
    childPwd='/'
    if pwd() is "/":
        childPwd = pwd() + selectedDir 
        
    else:
        childPwd = pwd() +"/"+selectedDir
    
    strings = ls(childPwd)
    row_num = len( strings )
    
    #boxChild.addstr( 25, 2, str( 61 ) + " - " + pwd()+selectedDir, highlightText )
    if  os.path.isfile(childPwd) or not os.access(childPwd, os.X_OK):
        boxChild.addstr( 1, 1, "Cannot Access", highlightText )
        boxChild.border( 0 )
        stdscr.refresh()
        boxChild.refresh()
        return boxChild

   
    pages = int( ceil( row_num / max_row ) )
    position = 1
    page = 1
    
    for i in range( 1, max_row  + 1 ):
        if row_num == 0:
            boxChild.addstr( 1, 1, "There aren't strings", highlightText )
        else:
            if (i == position):
                boxChild.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
            else:
                boxChild.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], normalText )
            if i == row_num:
                break

    #stdscr.refresh()
    boxChild.refresh()
   
    #boxParent.erase()
    #stdscr.border( 0 )
    boxChild.border( 0 )

    return boxChild


    # stdscr.refresh()
    # boxParent.refresh()




#######################################

def drawParent(stdscr): #sol menü 

    height, width = stdscr.getmaxyx()

    start_x = int((width // 2))
    start_y = int((height // 2) - 2)
    maxCol=width // 3-3
    max_row = height-5 #max number of rows
    boxParent = curses.newwin( max_row + 2, maxCol, 1, 1 )
    boxParent.box()

    
    highlightText = curses.color_pair( 2 )
    normalText = curses.A_NORMAL

    strings = lsP(pwd())
    row_num = len( strings )    
    

    statusbarstr = "Press 'q' to exit | STATUS BAR "
    # Render status bar
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height-1, 0, statusbarstr)
    stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    stdscr.attroff(curses.color_pair(3))
    
   
    pages = int( ceil( row_num / max_row ) )
    position = 1
    page = 1
    
    for i in range( 1, max_row  + 1 ):
        if row_num == 0:
            boxParent.addstr( 1, 1, "There aren't strings", highlightText )
        else:
            if strings[i -1] == pwd().split('/')[-1]: #l
                #boxParent.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
                boxParent.addstr( i, 2, str( i ) + " - " + pwd().split('/')[-1], highlightText )
            else:
                boxParent.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], normalText )
            if i == row_num:
                break

    #stdscr.refresh()
    boxParent.refresh()
   
    #boxParent.erase()
    #stdscr.border( 0 )
    boxParent.border( 0 )

    return boxParent


    # stdscr.refresh()
    # boxParent.refresh()