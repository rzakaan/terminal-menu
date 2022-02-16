import sys, os, subprocess

#####################
##### VARIABLES #####
#####################

mainMenus=["Main", "Settings", "Exit"]

class Font:
    REGULAR   = '0'
    BOLD      = '1'
    ITALIC    = '3'
    UNDERLINE = '4'
    BLINK     = '5'
    INVERT    = '7'
    
class FgColor:
    black   = ";30m"
    red     = ";31m"
    green   = ";32m"
    yellow  = ";33m"
    blue    = ";34m"
    magenta = ";35m"
    cyan    = ";36m"
    white   = ";37m"
    unknown = ";38m"
    default = ";39m"

class BgColor:
    black   ="\033[40m"
    red     ="\033[41m"
    green   ="\033[42m"
    yellow  ="\033[43m"
    blue    ="\033[44m"
    magenta ="\033[45m"
    cyan    ="\033[46m"
    white   ="\033[47m"
    unknown ="\033[48m"
    default ="\033[49m"
    reset   ="\033[49m"

class Settings:
    current_font = ""
    current_fg_color = ""
    current_bg_color = ""

#####################
### BASH FUNCTION ###
#####################

def bash(command):
    return os.popen(command).read().strip()    

def clearScreen(realClean=False):
    if realClean:
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
    setColor(FgColor.default)
    setBgColor(BgColor.default)
    setCursorBlink(True)


#####################
### MENU FUNCTION ###
#####################

def showSettings(menu):
    cols, lines = getCursor()
    moveCursor(lines, 0)
    storeCursor()
    val = input(":")
    if val == "set":
        pass
    clearScreen()
    restoreCursor()

def showMenu(menu, options, info, multiple=False, selected=[]):
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
        setColor(FgColor.white)
        setBgColor(BgColor.blue)
        print("  "  + menu + "  ")
        setColor(FgColor.default)
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
                setColor(FgColor.cyan)
            
            print("{option}".format(option=option))
            
            setFont(Font.REGULAR)
            setColor(FgColor.default)
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
            showSettings(menu)

def showList(name, list, info="", multiple=False, selected=[]):
    return showMenu(name, list, info, multiple, selected)
    
def showMainMenu():
    return showList("Main", mainMenus)


#####################
### CORE FUNCTION ###
#####################


        
#####################
### MAIN FUNCTION ###
#####################

def exitScript():
    setCursorBlink(True)
    sys.stdout.write("\033[0m")
    sys.exit()

def init():
    setCursorBlink(False)
    setFont(Font.REGULAR)
    setColor(FgColor.cyan)

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