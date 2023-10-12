import time
from rich import print
from rich.console import Group, Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from termcolor import colored
import keyboard
import mysql.connector

# Tietokantayhteys
yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='KierukkaKupariNöö7!',
    autocommit=True
)


# Backlore printtaus
def lore():
    backlore = Group(
        Panel("Medihelipeli: A Race Against Time", style="on blue"),
        Panel("You are a pilot for the No. 330 Squadron RNoAF emergency rescue helicopter. "
          f"The game is based on the beautiful landscape of Norway. \n\nYou are on a mission to save 12 patients with different kinds of injuries. "
          f"\n\nYour helicopter has a limited fuel capacity, so you have to be very strategic about what moves you make. "
          f"For each rescued patient you gain more fuel to save more patients. "
          f"\n\nIf you manage to save every patient before the fuel runs out, "
          f"\nyou`re hailed as a hero of the skies of Norway and different generations are going to tell stories about your courage. "
          f"\n\nBut if your fuel runs out before you manage to complete all of the rescue missions, your journey ends and the rest of the patients face uncertain fate.", style="on red"),
    )

    print(Panel(backlore))
    return





# Formatted_notitle -tyyli
def formatted_notitle(text):
    console = Console()
    formatted_text = colored(text, "blue")
    table = Table(show_header=False, width=75)
    table.add_row(formatted_text)
    console.print(table)

# Colored_text -tyyli
def colored_text(text, color):
    text_color = color
    bold = "\033[1m"
    reset = "\033[0m"
    formatted_text = f"{text_color}{bold}{text}{reset}"
    print(formatted_text)

# Input field Icao-koodin syöttämiseen
def input_field(title, text):
    input_field = Text(text)
    input_panel = Panel(input_field, title=title, style="on blue", padding=(0, 2), width=75)
    print(input_panel)

    # Käyttäjän syöte
    user_input = input("Your input: ")
    return user_input

# Tyylien määrittely Game rules -paneliin
def cool_field(title, text):
    input_field = Text(text, style="blue")
    input_panel = Panel(input_field, title=title, style="on blue", padding=(0, 2))
    print(input_panel)

# Tyylien määrittely Markdown -tyyliin
def markdown(text, color):
    bold = "\033[1m"
    reset = "\033[0m"
    markdown_text = f"""• {text}"""
    formatted_text = f"{color}{markdown_text}{reset}"
    print(formatted_text)

# Norway map
text1 = """         
                                                       _____________~-_
                                                     _/                >
                                                 __--             ___-~
                                                /            _,-_ `---_,
                                          _--\ /            /    `--\ /
                                         /    *            |        ,'
                             Harstad/'\ \  Tromså        (        (
                                   /'   \/      _/\___    /        /
                                 /'_,-      ___/ \_   `\/         |
                               /'/'  _/  . /       ~~\             \_
                              /`'   /    _/           |              \\
                                   /.  _/              \              |
                                 _/                     )            (
                               _/    /                  \             |
                              /     /                   /             |
                            _/     /                    \             \\
                           /      |                 ,----+-.           (
             Sandnessjån  /      /                .'        )           \_
                        _/      |                 |         \            (
                       /       /                  |        /~
               Namsos_/       |                   >       / FINLAND
                  __/         _)                 /       /
              ___/    .    /~~  SWEDEN          /      /
Kristiansund__/  Trondheim/                    _/      /
    Molde,/              |                    /      .'
 Ålesund/                |                  /       |
       |      NORWAY     |                 /        |
       \____   Lillehammer|                /         |
  Fårde,----'       Ål   /               (          |               ___---
       |         Elverum\                \        __,--~~
       |.       Hånefoss \                 \      _   ~-_  _*~        
       |            Oslo /                  \    <_>     ~---~~
       |     Drammen    |                    >                      ______
       `\      Skien|\  |Tånsberg          /                _-*~~~~
Haugesund`.        /   \|                 /~              <><
    Stavanger   ,Arendal\              _/     __          <__>\   ESTONIA
           `\___/Kristiansand           /      < /             \\"""

# Tulostaa korjan
def norway_map():
    console = Console()

    lines1 = text1.split('\n')
    # Tehdään taulu
    table = Table(expand=True)
    # Säädetään taulukon leveys
    table.add_column("Map of Norway", width=120)
    # Lisätään sisältö
    table.add_row('\n'.join(lines1))
    console.print(table)


# Värit
blue = "\033[95m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[33m"
pink = "\033[36m"
warning = '\033[93m'
bold = '\033[1m'
underline = '\033[4m'
reset = "\033[0m"

# Hakee ja palauttaa screen namen tietokannasta
def screen_name():
    sql = "SELECT screen_name FROM player WHERE id = 1"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    hero_name = cursor.fetchone()[0].upper()
    return hero_name



# Muuttujat dialogeihin
patient_name = 'WOMAN'
hero_name = 'PLAYER'
warning_text = 'Warning!'
dispatcher = 'DISPATCHER'
neutral = '**'

# Dialogi pohja
def dialogue_template(text, sex):
    if sex == patient_name:
        dialogue_text = f"{red}[{sex}]:{reset} {text}"
    elif sex == hero_name:
        dialogue_text = f"{green}[{screen_name()}]:{reset} {text}"
    elif sex == warning_text:
        dialogue_text = f"\n{bold}{warning}{underline}{sex}{reset}\n{text}"
    elif sex == dispatcher:
        dialogue_text = f"{red}[{sex}]:{reset} {text}"
    elif sex == neutral:
        dialogue_text = f"\n{warning}{text}{reset}"
    for char in dialogue_text:
        print(char, end='', flush=True)
        time.sleep(0.04)  # Adjust the typing speed
    time.sleep(0.5)
    return

# Puheenvuoro-muuttujat dialogeihin
time.sleep(0.5)

start1 = "(phone ringing...)\n\n"
start3 = "Yes, hello, what's up?\n\n"
start4 = ("The worst winterstorm of the century is approaching rapidly.\nWe need all the talented pilots like you in line. \n\n")
start5 = "Of course. I'm always ready for a rescue mission.\n\n"

acute1 = "(phone ringing...)\n\n"
acute3 = "Hi, yes, it's demanding but manageable. \nIs there something acute happening or why are you calling?\n\n"
acute4 = "There has been an avalanche with victims - can you please help with these patients immediately?\n\n"
acute5 = "Of course. I will pick up the victims right away and bring them to the home base.\n\n"


situation = 'Oh no! You are almost nearing the end of the mission but one of your patients is having an asthma attack...\n\n'

final1 = "(panicking) - Help, I can't breathe!\n\n"
final2 = "(rushing over) - What happened?\n\n"
final3 = "There is an inhaler in my bag! Help me please!\n\n"
final4 = "(searching the inhaler) - Fuck, I can't find it.\n\n"
final5 = "Hurry! (choking starts)\n\n"
final6 = "(retrieving the inhaler) - Got it. Take a deep breath. I'll help you use it.\n\n"
final7 = "(breathing heavily) - Thank you.\n\n"
final8 = "You're doing great. Fortunately everything went good.\n\n"

# Alun dialogi
def dialogue_start():
    for i in range(150):
        keyboard.block_key(i)
    if screen_name() == 'DR. MCLOVIN':
        start2 = f"Hello Dr. McLovin, can you hear? The signal has been unstable today.\n\n"
        start6 = f"You're a gift, Dr. McLovin! I'll send you the instructions shortly.\n\n"
    else:
        start2 = f"Hello {screen_name().lower().capitalize()}, can you hear? The signal has been unstable today.\n\n"
        start6 = f"You're a gift, {screen_name().lower().capitalize()}! I'll send you the instructions shortly.\n\n"
    dialogue_template(start1, neutral)
    dialogue_template(start2, dispatcher)
    dialogue_template(start3, hero_name)
    dialogue_template(start4, dispatcher)
    dialogue_template(start5, hero_name)
    dialogue_template(start6, dispatcher)
    for i in range(150):
        keyboard.unblock_key(i)
        
# Avalanche dialogi
def dialogue_avalanche():
    for i in range(150):
        keyboard.block_key(i)
    if screen_name() == 'DR. MCLOVIN':
        acute2 = f"Hello, Dr. McLovin - hope you are still safe despite the harsh conditions.\n\n"
    else:
        acute2 = f"Hello, {screen_name().lower().capitalize()} - hope you are still safe despite the harsh conditions.\n\n"
    dialogue_template(acute1, neutral)
    dialogue_template(acute2, dispatcher)
    dialogue_template(acute3, hero_name)
    dialogue_template(acute4, dispatcher)
    dialogue_template(acute5, hero_name)
    for i in range(150):
        keyboard.unblock_key(i)


# Lopun 1. dialogi
def dialogue_final_before():
    for i in range(150):
        keyboard.block_key(i)
    dialogue_template(situation, warning_text)
    dialogue_template(final1, patient_name)
    dialogue_template(final2, hero_name)
    dialogue_template(final3, patient_name)
    for i in range(150):
        keyboard.unblock_key(i)

# Lopun 2. dialogi
def dialogue_final_after():
    for i in range(150):
        keyboard.block_key(i)
    dialogue_template(final4, hero_name)
    dialogue_template(final5, patient_name)
    dialogue_template(final6, hero_name)
    dialogue_template(final7, patient_name)
    dialogue_template(final8, hero_name)
    for i in range(150):
        keyboard.unblock_key(i)

