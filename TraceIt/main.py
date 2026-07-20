import os
import time

import utils
import scripts

from utils import color
from utils import promptInput
from utils import clearTerminal

from scripts import lookupIp
from scripts import lookupNum
from scripts import checkEmail
from scripts import loginfo

options = ["Ip lookup", "Phone number lookup", "Validate email", "Log info", "Exit"]

def renderMenu():
    while True:
        clearTerminal()

        for index, label in enumerate(options, start=1):
            bracket1 = color('[', 'base')
            bracket2 = color(']', 'base')
            
            if label.lower() == "exit":
                index = "Q"
            print(f"{bracket1}{index}{bracket2} {label}")
        
        print(f"\n")

        choice = promptInput(f"Your choice?")

        if choice.lower() == "q":
            clearTerminal()
            print("\nGoodbye boss ;(")
            time.sleep(3)
            break
        elif choice == "1":
            clearTerminal()
            lookupIp() 
        elif choice == "2":
            clearTerminal()
            lookupNum()
        elif choice == "3":
            clearTerminal()
            checkEmail()
        elif choice == "4":
            clearTerminal()
            loginfo()
renderMenu()
