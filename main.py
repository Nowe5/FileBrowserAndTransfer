import sys, os
import curses
import subprocess
from math import *


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



def drawParent(stdscr):

    height, width = stdscr.getmaxyx()

    start_x = int((width // 2))
    start_y = int((height // 2) - 2)
    maxCol=width // 3-3
    max_row = height-5 #max number of rows
    boxParent = curses.newwin( max_row + 2, maxCol, 1, 1 )
    boxParent.box()

    
    highlightText = curses.color_pair( 2 )
    normalText = curses.A_NORMAL

    list_ls = lsP(pwd())
    strings = list_ls
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

    stdscr.refresh()
    boxParent.refresh()
   
    #boxParent.erase()
    #stdscr.border( 0 )
    boxParent.border( 0 )

 


    # stdscr.refresh()
    # boxParent.refresh()
    

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the stdscr for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    stdscr.keypad( 1 )
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
    #stdscr.border( 0 )
    curses.curs_set( 0 )

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)

    # Loop where k is the last character pressed
    #while (k != ord('q')):

    # Initialization
    stdscr.clear()


    
    drawPwdLs(stdscr)
    
    
    # Refresh the stdscr
    #stdscr.refresh()

    # Wait for next input
    #k = stdscr.getch()




def drawPwdLs(stdscr):
    height, width = stdscr.getmaxyx()

    start_x = int((width // 2))
    start_y = int((height // 2) - 2)
    maxCol=width // 3-3
    max_row = height-5 #max number of rows
    box = curses.newwin( max_row + 2, maxCol, 1, start_x - maxCol//2 )
    box.box()
    drawParent(stdscr)
    
    highlightText = curses.color_pair( 2 )
    normalText = curses.A_NORMAL
    ourPwd = pwd()
    list_ls = ls(ourPwd)
    strings = list_ls
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
            box.addstr( 1, 1, "There aren't strings", highlightText )
        else:
            if (i == position):
                box.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
            else:
                box.addstr( i, 2, str( i ) + " - " + strings[ i - 1 ], normalText )
            if i == row_num:
                break

    stdscr.refresh()
    box.refresh()
    x = stdscr.getch()

    while x != ord('q'):
                 
        if x == curses.KEY_DOWN:
            if page == 1:
                if position < i:
                    position = position + 1
                else:
                    if pages > 1:
                        page = page + 1
                        position = 1 + ( max_row * ( page - 1 ) )
            elif page == pages:
                if position < row_num:
                    position = position + 1
            else:
                if position < max_row + ( max_row * ( page - 1 ) ):
                    position = position + 1
                else:
                    page = page + 1
                    position = 1 + ( max_row * ( page - 1 ) )
        if x == curses.KEY_UP:
            if page == 1:
                if position > 1:
                    position = position - 1
            else:
                if position > ( 1 + ( max_row * ( page - 1 ) ) ):
                    position = position - 1
                else:
                    page = page - 1
                    position = max_row + ( max_row * ( page - 1 ) )
        
        if x == curses.KEY_LEFT:            
            # eğer / daysak sol a gitmesini engelle
            ourPwd = ourPwd[:ourPwd.rfind("/")]

            if ourPwd:
                ourPwd = '/'
                
            list_ls = ls( ourPwd )
            strings = list_ls
            row_num = len( strings )
            stdscr.refresh()
            box.refresh()
            

        if x == curses.KEY_RIGHT:
            ourPwd += '/' + strings[position -1]
            list_ls = ls( ourPwd )
            strings = list_ls
            row_num = len( strings )
            stdscr.refresh()
            box.refresh()
            pages = int( ceil( row_num / max_row ) )
            position = 1
            page = 1

        
        if x == ord( "\n" ) and row_num != 0:
            stdscr.erase()
            #stdscr.border( 0 )
            stdscr.addstr( 14, 3, "YOU HAVE PRESSED '" + strings[ position - 1 ] + "' ON POSITION " + str( position ) )

        box.erase()
        #stdscr.border( 0 )
        box.border( 0 )

        for i in range( 1 + ( max_row * ( page - 1 ) ), max_row + 1 + ( max_row * ( page - 1 ) ) ):
            if row_num == 0:
                box.addstr( 1, 1, "There aren't strings",  highlightText )
            else:
                if ( i + ( max_row * ( page - 1 ) ) == position + ( max_row * ( page - 1 ) ) ):
                    box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + strings[ i - 1 ], highlightText )
                else:
                    box.addstr( i - ( max_row * ( page - 1 ) ), 2, str( i ) + " - " + strings[ i - 1 ], normalText )
                if i == row_num:
                    break


        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        stdscr.refresh()
        box.refresh()
        x = stdscr.getch()

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the stdscr for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    stdscr.keypad( 1 )
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
    #stdscr.border( 0 )
    curses.curs_set( 0 )

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)

    # Loop where k is the last character pressed
    #while (k != ord('q')):

    # Initialization
    stdscr.clear()


    
    drawPwdLs(stdscr)
    
    
    # Refresh the stdscr
    #stdscr.refresh()

    # Wait for next input
    #k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()