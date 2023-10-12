import time
from rich import print
from rich.console import Group, Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from termcolor import colored


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





# ////////////////////////////////////////
def formatted_notitle(text):
    # Create a Console object
    console = Console()

    formatted_text = colored(text, "blue")

    # Create a table
    table = Table(show_header=False, width=75)

    # Add the text to the table
    table.add_row(formatted_text)

    # Print the table with a cool font
    console.print(table)

def colored_text(text, color):
    text_color = color #color can be changed - ?m
    bold = "\033[1m"
    reset = "\033[0m"

    # Combine the escape codes with the text
    formatted_text = f"{text_color}{bold}{text}{reset}"

    # Print the colored and underlined text
    print(formatted_text)

# /////////////////////////////////////////////////////////
# input type shit

def input_field(title, text):
    input_field = Text(text)

    # Create a Panel with the input field and style it
    input_panel = Panel(input_field, title=title, style="on blue", padding=(0, 2), width=75)

    # Print the input panel
    print(input_panel)

    # Get user input
    user_input = input("Your input: ")
    return user_input

def cool_field(title, text):
    input_field = Text(text, style="blue")

    # Create a Panel with the input field and style it
    input_panel = Panel(input_field, title=title, style="on blue", padding=(0, 2))

    # Print the input panel
    print(input_panel)

def markdown(text, color):
    bold = "\033[1m"
    reset = "\033[0m"
    markdown_text = f"""• {text}"""

    # Combine the escape codes with the text
    formatted_text = f"{color}{markdown_text}{reset}"

    # Print the colored and underlined text
    print(formatted_text)

# ////
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

def norway_map():
    console = Console()

    lines1 = text1.split('\n')

    # Tehdään taulu
    table = Table(expand=True)

    # Säädetään taulukon leveys
    table.add_column("Map of Norway", width=120)

    # lisätään sisältö
    table.add_row('\n'.join(lines1))

    console.print(table)


# ///////////////////////////////////////
blue = "\033[95m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[33m"
pink = "\033[36m"
warning = '\033[93m'
bold = '\033[1m'
underline = '\033[4m'
reset = "\033[0m"

patient_name = 'WOMAN'
hero_name = 'HERO'
warning_text = 'Warning!'

def finalboss_dialogue(text, sex):
    if sex == patient_name:
        dialogue_text = f"{red}[{sex}]:{reset} {text}"
    elif sex == hero_name:
        dialogue_text = f"{green}[{sex}]:{reset} {text}"
    elif sex == warning_text:
        dialogue_text = f"\n{bold}{warning}{underline}{sex}{reset}\n{text}"
    for char in dialogue_text:
        print(char, end='', flush=True)
        time.sleep(0.04)  # Adjust the typing speed
    time.sleep(0.5)

    # Define the text
situation = 'Oh no! You are almost nearing the end of the mission but one of your patients is having an asthma attack...\n\n'
time.sleep(0.5)
dialogue1 = f"(panicking) - Help, I can't breathe!\n\n"
dialogue2 = "(rushing over) - What happened?\n\n"
dialogue3 = "There is an inhaler in my bag! Help me please!\n\n"
dialogue4 = "(searching the inhaler) - Fuck, I can't find it.\n\n"
dialogue5 = "Hurry! (choking starts)\n\n"
dialogue6 = "(retrieving the inhaler) - Got it. Take a deep breath. I'll help you use it.\n\n"
dialogue7 = "(breathing heavily) - Thank you.\n\n"
dialogue8 = "You're doing great. Fortunately everything went good.\n\n"

    # Apply the typewriter effect without colors
def dialogue_print_before():
    finalboss_dialogue(situation, warning_text)
    finalboss_dialogue(dialogue1, patient_name)
    finalboss_dialogue(dialogue2, hero_name)
    finalboss_dialogue(dialogue3, patient_name)

def dialogue_print_after():
    # print(f"[{patient_name}]: (panicking) - Help, I can't breathe!\n\n[{hero_name}]: (rushing over) - What happened?\n\n"
    #       f"[{patient_name}]: There is an inhaler in my bag! Help me please!\n\n")
    finalboss_dialogue(dialogue4, hero_name)
    finalboss_dialogue(dialogue5, patient_name)
    finalboss_dialogue(dialogue6, hero_name)
    finalboss_dialogue(dialogue7, patient_name)
    finalboss_dialogue(dialogue8, hero_name)
