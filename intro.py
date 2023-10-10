import time
import os
import mysql.connector

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='KierukkaKupariNöö7!',
    autocommit=True
)

class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

# INTRO

def intro():
    # Define the frames for the helicopter and symbols
    helicopter_frame = [
        Colors.CYAN +    "   ▬▬▬▬▬.◙.▬▬▬▬▬    __________  ___    ___________________      __________             __________ ",
        Colors.RED +     "      ▂▄▄▓▄▄▂              _______   |/  /__________  /__(_)__  /_________  /__(_)_______________  /__(_)",
        Colors.GREEN +   "   ◢◤█▀▀████▄▄▄▄▄▄ ◢◤    ______  /|_/ /_  _ \\  __  /__  /__  __ \\  _ \\_  /__  /___  __ \\  _ \\_  /__  /",
        Colors.YELLOW + "   █▄ █ █▄ ███▀▀▀▀▀▀▀ ╬    _____  /  / / /  __/ /_/ / _  / _  / / /  __/  / _  / __  /_/ /  __/  / _  / ",
        Colors.BLUE +   "   ◥ █████ ◤              ____/_/  /_/  \___/\__,_/  /_/  /_/ /_/\___//_/  /_/  _  .___/\___//_/  /_/ ",
        Colors.BLUE +   "    ══╩══╩═                                                                      /_/                     ",
        Colors.CYAN
    ]

    symbol_frames = ["      ╬═╬"] * 1


    # Clear the terminal screen function (for Windows and Unix-like systems)
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    # Animation loop
    while True:
        for frame in helicopter_frame:
            clear_screen()
            print(frame)
            time.sleep(0.1)

        for _ in range(5):
            clear_screen()
            for symbol_frame in symbol_frames:
                print(symbol_frame)
                time.sleep(0.1)
        print("     ☻/  - Hello, are you ready for an adventure?")
        time.sleep(0.1)
        print("     /▌")
        time.sleep(0.1)
        print("     / \\")
        print(Colors.RESET)
        break
    return

