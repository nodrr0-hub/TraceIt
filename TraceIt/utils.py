import fade
from colorama import Fore, Style
import os
from datetime import datetime



colors = {
    'base': Fore.RED,
    'label': Fore.LIGHTBLUE_EX,
    'secondary': Fore.LIGHTRED_EX
}

banner = """
                    
                    
                    ░██████████                                             ░██████   ░██    
                        ░██                                                   ░██     ░██    
                        ░██    ░██░████  ░██████    ░███████   ░███████       ░██  ░████████ 
                        ░██    ░███           ░██  ░██    ░██ ░██    ░██      ░██     ░██    
                        ░██    ░██       ░███████  ░██        ░█████████      ░██     ░██    
                        ░██    ░██      ░██   ░██  ░██    ░██ ░██             ░██     ░██    
                        ░██    ░██       ░█████░██  ░███████   ░███████     ░██████    ░████       

                                            </> developer: n0dr

"""


def renderBanner():
    print(color(banner, 'base'))


def color(val, paint):
    val = str(val)
    return colors[paint] + val + Style.RESET_ALL


def promptInput(query):
    query = str(query)
    return input(color(f"[ {query} ]: ", 'base'))


def formatDebug(label, val):
    now = datetime.now()
    now_time = f"--[{now.strftime("%H:%M:%S")}] "

    label = color(now_time + label, 'label')
    val = color(val, 'secondary')
    return f"{label}: {val}"

def formatErr(msg):
    return f"{color('!Error:', 'secondary')} {msg}"


def clearTerminal():
    os.system("cls")
    renderBanner()