#!/usr/bin/python

import sys, os, subprocess

main_menu=["Main", "Settings", "Exit"]

class Font:
    REGULAR   = '0'
    BOLD      = '1'
    ITALIC    = '3'
    UNDERLINE = '4'
    BLINK     = '5'
    INVERT    = '7'
    
class FgColor:
    BLACK   = ';30m'
    RED     = ';31m'
    GREEN   = ';32m'
    YELLOW  = ';33m'
    BLUE    = ';34m'
    MAGENTA = ';35m'
    CYAN    = ';36m'
    WHITE   = ';37m'
    UNKNOWN = ';38m'
    DEFAULT = ';39m'

class BgColor:
    BLACK   = '\033[40m'
    RED     = '\033[41m'
    GREEN   = '\033[42m'
    YELLOW  = '\033[43m'
    BLUE    = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN    = '\033[46m'
    WHITE   = '\033[47m'
    UNKNOWN = '\033[48m'
    DEFAULT = '\033[49m'

class Settings:
    current_font = ""
    current_fg_color = ""
    current_bg_color = ""

#--------------------
# SHELL FUNCTIONS
#--------------------

def bash(command):
    '''
    Allows you to run the given command in shell.

    Parameters
    ----------
    command : str
        shell command
        
    Return
    ------
    stdout of shell command 
    '''
    return os.popen(command).read().strip()    

def clearScreen(reset=False):
    '''
    Clear screen

    Parameters
    ----------
    realClean : bool, optional
        Reset all terminal settings to default.
    '''
    if reset:
        os.system("printf \033c")
    else:
        os.system("clear")

def readKey():
    global process
    process = os.popen('bash ./read.sh')
    key = process.read()

    if len(key) > 1:
        key=key.strip()

    if key == '[A':
        val="up"
    elif key == '[B':
        val="down"
    elif key == '[C':
        val="right"
    elif key == '[D':
        val="left"
    elif key == '[H':
        val="home"
    elif key == '[F':
        val="end"
    elif key == '\n':
        val="enter"
    else:
        val=key
    
    return val

def moveCursor(x, y):
    sys.stdout.write("\033[" + str(x) + ";" + str(y) + "H")
    
def getCursor():
    lines = os.popen('x=$(tput lines); echo $x').read()
    cols =  os.popen('x=$(tput cols); echo $x').read()
    return cols, lines
    
def storeCursor():
    sys.stdout.write("\033[s")
    
def restoreCursor():
    sys.stdout.write("\033[u")

def setCursorBlink(v):
    if v:
        sys.stdout.write("\033[?25h")
    else:
        sys.stdout.write("\033[?25l")

def setTerm():
    fg_color = "\033[" + Settings.current_font + Settings.current_fg_color
    sys.stdout.write(fg_color)
    sys.stdout.write(Settings.current_bg_color)

def setFont(font):
    Settings.current_font = font
    setTerm()

def setBgColor(color):
    Settings.current_bg_color = color
    setTerm()

def setColor(color):
    #
    # tty font color
    # \033[ + font + color + m
    # \033[0;30m
    #

    Settings.current_fg_color = color
    setTerm()

def setDefaultColor():
    setColor(FgColor.DEFAULT)
    setBgColor(BgColor.default)
    setCursorBlink(True)


#--------------------
# MENU FUNCTIONS
#--------------------

def showSettings():
    cols, lines = getCursor()
    moveCursor(lines, 0)
    storeCursor()
    val = input(":")
    if val == "set":
        pass
    clearScreen()
    restoreCursor()

def showMenu(title, options, info='', multiple=False, selected=[]):
    loop=True
    currentIndex=0
    lastIndex=len(options)
    selection=[]
    clearScreen()
    setCursorBlink(False)

    for o in options:
        if o in selected:
            selection.append(o)

    while loop:
        moveCursor(0,3)
        setColor(FgColor.WHITE)
        setBgColor(BgColor.blue)
        print("  "  + title + "  ")
        setColor(FgColor.DEFAULT)
        setBgColor(BgColor.default)
        print("")
        
        if info != "":
            print(3 * " " + info)
            print("")
            
        for idx, option in enumerate(options):
            sys.stdout.write(2 * " ")
            if currentIndex == idx:
                setFont(Font.INVERT)
            else:
                setFont(Font.REGULAR)
                setBgColor(BgColor.default)

            if option in selection:
                setColor(FgColor.CYAN)
            
            print("{option}".format(option=option))
            
            setFont(Font.REGULAR)
            setColor(FgColor.DEFAULT)
            setBgColor(BgColor.default)

        key = readKey()
        
        if key == "up":
            if currentIndex == 0:
                currentIndex = lastIndex - 1
            else:
                currentIndex -= 1
        
        elif key == "down":
            if currentIndex == lastIndex - 1:
                currentIndex = 0
            else:
                currentIndex += 1
            
        elif key == "right" or key == "enter":
            if multiple:
                return selection
            else:
                return options[currentIndex]

        elif key == "home":
            currentIndex = 0
    
        elif key == "end":
            currentIndex = lastIndex -1
                        
        elif key == "s" or key == "x" and multiple:
            if options[currentIndex] not in selection:
                selection.append(options[currentIndex])
            else:
                selection.remove(options[currentIndex])
        
        elif key == "c":
            if multiple:
                selection=[]
        
        elif key == "r":
            for o in options:
                if o in selected:
                    selection.append(o)
        
        elif key == ":":
            showSettings(title)

def showMainMenu():
    return showMenu('Main', main_menu)  
      
#--------------------
# MAIN FUNCTION
#--------------------

def exitScript():
    setCursorBlink(True)
    sys.stdout.write("\033[0m")
    sys.exit()

def init():
    setCursorBlink(False)
    setFont(Font.REGULAR)
    setColor(FgColor.CYAN)

def main():
    init()
    while True:
        try:
            idx=showMainMenu()
            if idx == "Main":
                pass
            elif idx == "Settings":
                pass
            elif idx == "Exit":
                exitScript()
        except KeyboardInterrupt:
            exitScript()
    
if __name__ == "__main__":
    main()