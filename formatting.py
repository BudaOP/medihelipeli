from rich import print
from rich.console import Group, Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from termcolor import colored


def lore():
    backlore = Group(
        Panel("Medihelipeli: A Race Against Time", style="on blue"),
        Panel("Time is running out. Equipped with an advanced emergency rescue helicopter No. 330 Squadron RNoAF,\n"
        "you are set on a dangerous patient-saving journey in the beautiful landscape of Norway.\n"
        "Your helicopter's fuel is limited, and each rescue mission consumes a significant portion of it.\n"
        "The goal is to save all twelve patients before you run out of fuel.\n"
        "Each rescue attempt must be carefully calculated to maximize fuel efficiency while minimizing the time taken to reach and rescue the patients.\n"
        "There are three kinds of danger levels (1-3). The level depends on the severity of the patient's injury.\n"
        "Depending on the severity of the injury, the level changes.\n"
        "If you manage to save all twelve patients within the fuel "
        "constraints, you're hailed as a hero, and the skies of Norway echo "
        "with the stories of your courage.\n"
        "However, if your fuel runs out before completing the rescue missions, "
        "your journey ends, and the fate of the remaining patients remains uncertain.", style="on red"),
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
    print('\n')
    input_field = Text(text)

    # Create a Panel with the input field and style it
    input_panel = Panel(input_field, title=title, style="on blue", padding=(0, 2), width=75)

    # Print the input panel
    print(input_panel)

    # Get user input
    user_input = input("Your input: ")
    print('*' * 75)
    return user_input

def cool_field(title, text):
    input_field = Text(text, style="blue")

    # Create a Panel with the input field and style it
    input_panel = Panel(input_field, title=title, style="on blue", padding=(0, 2))

    # Print the input panel
    print(input_panel)

def markdown(text):
    color = "\033[92m" #color can be changed - ?m
    bold = "\033[1m"
    reset = "\033[0m"
    markdown_text = f"""• {text}"""

    # Combine the escape codes with the text
    formatted_text = f"{color}{bold}{markdown_text}{reset}"

    # Print the colored and underlined text
    print(formatted_text)
