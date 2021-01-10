from func import *
#from ssh import *


def drawPwdLs(stdscr): #orta menü
    height, width = stdscr.getmaxyx()
    start_x = int((width // 2))
    start_y = int((height // 2) - 2)
    maxCol=width // 3-3
    max_row = height-5 #max number of rows
    
    highlightText = curses.color_pair( 2 )
    normalText = curses.A_NORMAL

    box = curses.newwin( max_row + 2, maxCol, 1, start_x - maxCol//2 )
    box.box()
    boxParent=drawParent(stdscr)
    
    
    #ssh > ssh connection > control server or client > change ranger >


    ourPwd = pwd()
    strings = ls(ourPwd)
    row_num = len( strings )

    boxChild = drawChild(stdscr, strings[0])
    
    statusbarstr = "Press 'q' to exit | STATUS BAR "

    # Render Top Status bar             #linuxta subprocess ile çalıştırmamız lazım bence username ve hostname i. ssh ile bağlandığımızda orda sadece terminal komutları çalıştıracağız çünkü.
    userName = os.environ['USER']
    hostName = socket.gethostname()
    statusPwd=ourPwd
    if statusPwd.startswith("/home/"+userName):
        statusPwd = statusPwd.replace("/home/"+userName, "~")
    stdscr.addstr(0, 2, userName+"@"+ hostName+" " +statusPwd+ "/" + strings[0])
    
    
    # Render Bottom Status bar
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height-1, 0, statusbarstr)    #statusbarstr
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
    boxParent.refresh()
    boxChild.refresh()
    x = stdscr.getch()  #bu box.getch() olabilir mi ? ama o zaman da quit mi olmaz bilemedim.

    while x != ord('q'):
                 
        if x == curses.KEY_DOWN and not row_num == 0:
            if page == 1:
                if position < i:
                    position = position + 1
                elif pages > 1:
                    page = page + 1
                    position = 1 + ( max_row * ( page - 1 ) )
            elif page == pages:
                if position < row_num:
                    position = position + 1
            elif position < max_row + ( max_row * ( page - 1 ) ):
                    position = position + 1
            else:
                page = page + 1
                position = 1 + ( max_row * ( page - 1 ) )
            refreshChild(boxChild, ourPwd, stdscr, strings[position -1])      #refreshChild(boxChild,ourPwd,stdscr,selectedDir)
        if x == curses.KEY_UP and not row_num == 0:
            if page == 1:
                if position > 1:
                    position = position - 1
            elif position > ( 1 + ( max_row * ( page - 1 ) ) ):
                position = position - 1
            else:
                page = page - 1
                position = max_row + ( max_row * ( page - 1 ) )
            refreshChild(boxChild, ourPwd, stdscr, strings[position -1])      #refreshChild(boxChild,ourPwd,stdscr,selectedDir)

  
        if x == curses.KEY_LEFT:    #sol oka basıldığında olanlar vs    #ourPwd nin uzunluğu 1 değilse çalıştırabiliriz belki     
            
            ourPwd = ourPwd[:ourPwd.rfind("/")] #pathin son slashtan sonrasını sil oraya git.

            if not ourPwd or len(ourPwd)<2:     #pathhte ki sorunları giderme
                ourPwd = '/'
                
            strings = ls( ourPwd )
            row_num = len( strings )
            
            #refreshParent return degeri position'a verildi. Dizinden devam etmek için.
            #TODO : position değeri dizinden devam ettirilecek.
            
            pages = int( ceil( row_num / max_row ) )
            position = 1
            page = 1
            
            refreshParent(boxParent,ourPwd,stdscr) #[:ourPwd.rfind("/")]
            refreshChild(boxChild, ourPwd, stdscr, strings[position -1])      #refreshChild(boxChild,ourPwd,stdscr,selectedDir)
            box.refresh()
            stdscr.refresh()

        if x == curses.KEY_RIGHT and not row_num == 0 and os.path.isdir(ourPwd+"/"+strings[position-1]):
             
            if not ourPwd or len(ourPwd)<2:     #pathhte ki sorunları giderme
                ourPwd = "/"+strings[position -1]
            else:
                ourPwd += '/' + strings[position -1]
            strings = ls( ourPwd )
            row_num = len( strings )
            
            pages = int( ceil( row_num / max_row ) )
            position = 1
            page = 1
            if row_num == 0:                    
                boxChild.erase()
                boxChild.refresh()
            else:
                refreshChild(boxChild, ourPwd,stdscr ,strings[position -1])      #refreshChild(boxChild,ourPwd,stdscr,selectedDir)
            
            refreshParent(boxParent,ourPwd,stdscr) #[:ourPwd.rfind("/")]
            box.refresh()
            stdscr.refresh()
        
        if x == ord("L") :
            cred=drawLogin(stdscr)
            
            
        #Enter a basınca yazan yazı
        # if x == ord( "\n" ) and row_num != 0:
        #     stdscr.erase()
        #     #stdscr.border( 0 )
        #     stdscr.addstr( 14, 3, "YOU HAVE PRESSED '" + strings[ position - 1 ] + "' ON POSITION " + str( position ) )

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
        
        statusPwd=ourPwd
        if statusPwd.startswith("/home/"+userName):
                statusPwd = statusPwd.replace("/home/"+userName, "~")
        #todo: status
        if row_num != 0:
            if len(statusPwd) != 1 or statusPwd.startswith('~'):
                stdscr.addstr(0, 2, userName+"@"+ hostName+" " +statusPwd + "/"+strings[position -1]+"\t\t\t\t\t" )  
            else:
                stdscr.addstr(0, 2, userName+"@"+ hostName+" " +statusPwd +strings[position -1]+"\t\t\t\t\t" )   # / dizininde iki kere / yazıyordu yani //bin gibi
            
        else:
            stdscr.addstr(0, 2, userName+"@"+ hostName+" " +statusPwd + "/"+"\t\t\t\t\t\t\t" ) 
        
            

        # Render Bottom Status bar
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
    try:
        curses.wrapper(draw_menu)
    except KeyboardInterrupt:
        #TODO close ssh connection bla bla
        pass

if __name__ == "__main__":
    main()