import sys, os, subprocess

#####################
####### NOTES #######
#####################

# subprocess.Popen non-blocking
# subprocess.call  blocking

#####################
##### VARIABLES #####
#####################

mainMenus=["Main", "Settings", "Exit"]

class Font:
    isRegular=True
    isBlink=False
    isInvert=False
    isBold=False
    isItalic=False
    isLine=False
    isUnderline=False

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

class Tx:
    current="\033[0;39m"
    
    reset   ="\033[0m"
    bold    ="\033[1m"
    underline ="\033[4m"
    blink   ="\033[5m"
    invert  ="\033[7m"
    
    # regular
    black   ="\033[0;30m"
    red     ="\033[0;31m"
    green   ="\033[0;32m"
    yellow  ="\033[0;33m"
    blue    ="\033[0;34m"
    magenta ="\033[0;35m"
    cyan    ="\033[0;36m"
    white   ="\033[0;37m"
    unknown ="\033[0;38m"
    default ="\033[0;39m"
    
    # bold and brights
    gray         ="\033[1;30m"
    bold_red     ="\033[1;31m"
    bold_green   ="\033[1;32m"
    bold_yellow  ="\033[1;33m"
    bold_blue    ="\033[1;34m"
    bold_magenta ="\033[1;35m"
    bold_cyan    ="\033[1;36m"
    bold_white   ="\033[1;37m"
    bold_unknown ="\033[1;38m"
    bold_default ="\033[1;39m"
    
    # underline
    under_black   ="\033[4;30m"
    under_red     ="\033[4;31m"
    under_green   ="\033[4;32m"
    under_yellow  ="\033[4;33m"
    under_blue    ="\033[4;34m"
    under_magenta ="\033[4;35m"
    under_cyan    ="\033[4;36m"
    under_white   ="\033[4;37m"
    under_unknown ="\033[4;38m"
    under_default ="\033[4;39m"

#####################
### DEBUG FUNCTION ##
#####################

def debugFont():
    print("Font.isRegular:"  + str(Font.isRegular))
    print("Font.isBold:"  + str(Font.isBold))
    print("Font.isItalic:"  + str(Font.isItalic))
    print("Font.isUnderline:"  + str(Font.isUnderline))
    print("Font.isBlink:"  + str(Font.isBlink))
    print("Font.isInvert:"  + str(Font.isInvert))
    print("Font.isline:"  + str(Font.isLine))

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
    # read key not use because illegal option
    # process = os.popen('read -rsn1 key && if [[ $key == $(printf "\033") ]]; then read -rsn2 key; fi; echo $key')
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

def setCurcorBlink(v):
    if v:
        sys.stdout.write("\033[?25h")
    else:
        sys.stdout.write("\033[?25l")

def setBlink():
    Font.isBlink=True
    Font.isRegular=False
    Font.isBold=False
    Font.isItalic=False
    Font.isUnderline=False
    sys.stdout.write(Tx.current)

def setRegular():
    Font.isRegular=True    
    Font.isBold=False
    Font.isBlink=False
    Font.isItalic=False
    Font.isUnderline=False
    sys.stdout.write(Tx.current)

def setBold():
    Font.isBold=True
    Font.isBlink=False
    Font.isItalic=False
    Font.isRegular=False
    Font.isUnderline=False
    sys.stdout.write(Tx.current)

def setItalic():
    Font.isItalic=True
    Font.isBlink=False
    Font.isBold=False
    Font.isRegular=False
    Font.isUnderline=False
    sys.stdout.write(Tx.current)
    
def setUnderline():
    Font.isUnderline=True
    Font.isBlink=False
    Font.isRegular=False
    Font.isBold=False
    Font.isItalic=False
    sys.stdout.write(Tx.current)
  
def setBgColor(c):
    sys.stdout.write(c)
    
def setColor(c):
    # old version
    sys.stdout.write(c)
    return
    
    # development
    color=c
    idx=color.find('[') + 1
    
    if Font.isRegular:
        cmd="0"
    elif Font.isBold:
        cmd="1"
    elif Font.isItalic:
        cmd="3"
    elif Font.isUnderline:
        cmd="4"
    elif Font.isBlink:
        cmd="5"
    elif Font.isInvert:
        cmd="7"
    elif Font.isLine:
        cmd="9"

    color = color[:idx] + cmd + color[idx+1:]
    Tx.current=c
    sys.stdout.write(color)
    
def setDefaultColor(c):
    setColor(Bg.default)
    setColor(Tx.default)
    setCursorBlink(True)
    
def defaultCursor():
    sys.stdout.write(Tx.reset)


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
    setCurcorBlink(False)

    for o in options:
        if o in selected:
            selection.append(o)

    while loop:
        moveCursor(0,3)
        setColor(Tx.white)
        setColor(BgColor.blue)
        print("  "  + menu + "  ")
        setColor(Tx.default)
        setColor(BgColor.default)
        print("")
        
        if info != "":
            print(3 * " " + info)
            print("")
            
        for idx, option in enumerate(options):
            sys.stdout.write(2 * " ")
            if currentIndex == idx:
                setColor(Tx.invert)
            else:
                setColor(BgColor.default)
                setColor(Tx.reset)
                
            if option in selection:
                setColor(Tx.cyan)
            
            print("{option}".format(option=option))
            
            setColor(BgColor.default)
            setColor(Tx.default)
            setColor(Tx.reset)
            
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
    setCurcorBlink(True)
    setColor(Tx.default)
    sys.exit()

def main():
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
    
main()




