white =                 "\033[1;37m"
yellow =                "\033[1;33m"
green =                 "\033[1;32m"
blue =                  "\033[1;34m"
cyan =                  "\033[1;36m"
red =                   "\033[1;31m"
magenta =               "\033[1;35m"
black =                 "\033[1;30m"
darkyellow =            "\033[0;33m"
darkblue =              "\033[0;34m"
darkmagenta =           "\033[0;35m"
darkblack =             "\033[0;30m"
clear =                 "\033[0;0m"

FAIL =                  "\033[91m"

BRIGHT    =             "\033[1m"
DIM       =             "\033[2m"
NORMAL    =             "\033[22m"
RESET_ALL =             "\033[0m"

BOLD =                  "\033[1m"
FAINT =                 "\033[2m"
ITALIC =                "\033[3m"
UNDERLINE =             "\033[4m"
BLINK =                 "\033[5m"
NEGATIVE =              "\033[7m"
CROSSED =               "\033[9m"

CURSOR_UP =             "\033[A"
CURSOR_ERASE_LINE =     "\033[K"

def printWhite       (content): print("\033[1;37m" + str(content) + "\033[0;0m")
def printYellow      (content): print("\033[1;33m" + str(content) + "\033[0;0m")
def printGreen       (content): print("\033[1;32m" + str(content) + "\033[0;0m")
def printBlue        (content): print("\033[1;34m" + str(content) + "\033[0;0m")
def printCyan        (content): print("\033[1;36m" + str(content) + "\033[0;0m")
def printRed         (content): print("\033[1;31m" + str(content) + "\033[0;0m")
def printMagenta     (content): print("\033[1;35m" + str(content) + "\033[0;0m")
def printBlack       (content): print("\033[1;30m" + str(content) + "\033[0;0m")
def printDarkyellow  (content): print("\033[0;33m" + str(content) + "\033[0;0m")
def printDarkblue    (content): print("\033[0;34m" + str(content) + "\033[0;0m")
def printDarkmagenta (content): print("\033[0;35m" + str(content) + "\033[0;0m")
def printDarkblack   (content): print("\033[0;30m" + str(content) + "\033[0;0m")

def printBOLD        (content): print("\033[1m"    + str(content) + "\033[0;0m")
def printFAINT       (content): print("\033[2m"    + str(content) + "\033[0;0m")
def printITALIC      (content): print("\033[3m"    + str(content) + "\033[0;0m")
def printUNDERLINE   (content): print("\033[4m"    + str(content) + "\033[0;0m")
def printBLINK       (content): print("\033[5m"    + str(content) + "\033[0;0m")
def printNEGATIVE    (content): print("\033[7m"    + str(content) + "\033[0;0m")
def printCROSSED     (content): print("\033[9m"    + str(content) + "\033[0;0m")

def printC           (content): print(               str(content) + "\033[0;0m")