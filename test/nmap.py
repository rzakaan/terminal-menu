import sys 
sys.path.append('./../src/')

import time, ipaddress, term

# list of menus
main_menu=["Install", "IP", "Scan", "Exit"]
scan_menu=["Ping", "TCP SYN", "UDP", "Idle", "Version"]

def currentIP():
    return term.shell("ifconfig | grep 'inet ' | grep -Fv 127.0.0.1 | awk '{print $2}'").splitlines()

def showMainMenu():
    return term.showMenu('Main', main_menu)  

def scanSelection():
    sel = term.showMenu('Scan Type', scan_menu)
    param = ""
    if sel == "Ping":
        param = "-sn"
    elif sel == "TCP SYN":
        param = "-sT"
    elif sel == "UDP":
        param = "-sU"
    elif sel == "Idle":
        param = "-sI"
    elif sel == "Version":
        param = "-sV"
    return param

def targetSelection(title="Target"):
    ips = currentIP()
    return term.showMenu(title, ips)

def waitKey():
    print("\npress a key to continue...")
    term.readKey()

def main():    
    term.init()
    while True:
        try:
            idx=showMainMenu()
            if idx == "Install":
                term.shell("brew install nmap", output=True)

            elif idx == "IP":
                targetSelection("IP")
                waitKey()

            elif idx == "Scan":
                param = scanSelection()
                ip = targetSelection()
                subnet_mask = "/24"
                ip_network = ipaddress.IPv4Network(ip + subnet_mask, strict=False)
                cmd ="nmap " + param + " " +  str(ip_network)
                term.shell(cmd, output=True)
                waitKey()
                
            elif idx == "Exit":
                term.exitScript()

        except KeyboardInterrupt:
            term.exitScript()
    
if __name__ == "__main__":
    main()