#!/usr/bin/python

import sys, os
import subprocess

VARS = {}
class CMD:
    READ = 'read -rsn 1 key && if [[ $key == $(printf "\033") ]]; then read -rsn 2 key; fi; echo $key'
    CUR_LINE = 'x=$(tput lines); echo $x'
    CUR_COLS = 'x=$(tput cols); echo $x'

class Font:
    REGULAR   = '0'
    BOLD      = '1'
    ITALIC    = '3'
    UNDERLINE = '4'
    BLINK     = '5'
    INVERT    = '7'
    
class FgColor:
    BLACK   = ";30m"
    RED     = ";31m"
    GREEN   = ";32m"
    YELLOW  = ";33m"
    BLUE    = ";34m"
    MAGENTA = ";35m"
    CYAN    = ";36m"
    WHITE   = ";37m"
    UNKNOWN = ";38m"
    DEFAULT = ";39m"

class BgColor:
    BLACK   = "\033[40m"
    RED     = "\033[41m"
    GREEN   = "\033[42m"
    YELLOW  = "\033[43m"
    BLUE    = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN    = "\033[46m"
    WHITE   = "\033[47m"
    UNKNOWN = "\033[48m"
    DEFAULT = "\033[49m"

class Settings:
    os_type = ""
    current_font = ""
    current_fg_color = ""
    current_bg_color = ""

#--------------------
# SHELL FUNCTIONS
#--------------------

def __windows_ansi():
    # For windows, calling os.system("") 
    # makes the ANSI escape sequence get processed correctly
    if os.name == "nt":
        os.system("color")

def shell(command, output=False):
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
    if output:
        res = ""
        try:
            with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, shell=True) as p:
                for line in p.stdout:
                    res += line
                    print(line, end='')            
        except subprocess.CalledProcessError:
            print("subprocess error !")
        
        return res
    else:
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

'''
    Enter key reading recommendation on macos
    global process
    process = os.popen('sh ../src/read.sh')
    key = process.read()

    or just press right arrow >
'''
def readKey():
    key = shell(CMD.READ)

    if len(key) > 1:
        key = key.strip()

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
    __windows_ansi()
    print("\033[%d;%dH" % (x, y))
    
def getCursor():
    lines = os.popen(CMD.CUR_LINE).read()
    cols =  os.popen(CMD.CUR_COLS).read()
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

def setVariable(param):
    idx = param.find('=')
    if not idx > 0:
        print("error set variable ")
    
    name = param[0 : idx].strip()
    value = param[idx + 1: len(param)].strip()
    VARS[name] = value

def getVariable(name):
    if name in VARS:
        return VARS[name]
    else:
        return ""

def showSettings(title):
    storeCursor()
    cols, lines = getCursor()
    moveCursor(int(lines), 0)
    string = input(":")
    i = string.find(' ')
    command = string[:i].lower()
    param = string[i + 1 : len(string)].strip()

    match command:
        case "set":
            setVariable(param)
            clearScreen()
        case "get":
            v = getVariable(param)
            moveCursor(int(lines) -1, 0)
            print(v)
            readKey()
    
    clearScreen()

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
        setBgColor(BgColor.BLUE)
        print("  "  + title + "  ")
        setColor(FgColor.DEFAULT)
        setBgColor(BgColor.DEFAULT)
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
                setBgColor(BgColor.DEFAULT)

            if option in selection:
                setColor(FgColor.CYAN)
            
            print("{option}".format(option=option))
            
            setFont(Font.REGULAR)
            setColor(FgColor.DEFAULT)
            setBgColor(BgColor.DEFAULT)

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
                        
        elif (key == "s" or key == "x") and multiple:
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
      
#--------------------
# MAIN FUNCTION
#--------------------

def exitScript():
    __windows_ansi()
    setCursorBlink(True)
    sys.stdout.write("\033[0m")
    sys.exit()

def init():
    __windows_ansi()
    setCursorBlink(False)
    setFont(Font.REGULAR)
    setColor(FgColor.CYAN)