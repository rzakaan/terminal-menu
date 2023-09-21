import sys, time
sys.path.append('./../src/')

import menu as term
term.clearScreen()

main_menu=["List", "Ping", "Exit"]

def showMainMenu():
    return term.showMenu('Main', main_menu)  

def waitKey():
    print("\npress a key to continue...")
    term.readKey()

def main():    
    term.init()
    while True:
        try:
            idx=showMainMenu()
            if idx == "List":
                term.clearScreen()
                term.shell("ls .", output=True)
                waitKey()

            elif idx == "Ping":
                term.clearScreen()
                term.shell("ping localhost -c 4", output=True)
                waitKey()

            elif idx == "Exit":
                term.exitScript()

        except KeyboardInterrupt:
            term.exitScript()
    
if __name__ == "__main__":
    main()