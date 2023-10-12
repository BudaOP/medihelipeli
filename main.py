import random
import mysql.connector
from mysql.connector import errorcode
from geopy import distance
from tabulate import tabulate
from termcolor import colored
from intro import intro
from formatting import lore, formatted_notitle, colored_text, input_field, cool_field, markdown, norway_map, dialogue_print_before, dialogue_print_after

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='KierukkaKupariNöö7!',
    autocommit=True
)

# Colors
blue = "\033[95m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[33m"
cyan = "\033[36m"
underline = '\033[4m'
warning = '\033[93m'
bold = '\033[1m'
reset = "\033[0m"


# FUNKTIOT

def start():
    screen_name = input("\nWhat's your name? "
                        "(Press enter to set a default hero name) \n"
                        "Type here: ")

    if screen_name == "":
        screen_name = "Dr. McLovin"

    sql_start = (f"UPDATE player SET screen_name = '{screen_name}', "
                 f"location = 'ENTR', patient_goal = 11, patient_qty = 0, "
                 f"range_km = 4000 WHERE id = 1")
    sql_start_patient = f"UPDATE patient SET rescued = 0"
    sql_start_quiz = f"UPDATE airport SET quiz = 0"
    sql_start_used = f"UPDATE quiz SET used = 0"
    cursor = yhteys.cursor()
    try:
        cursor.execute(sql_start)
    except mysql.connector.ProgrammingError as err:
        print(f"{red}Invalid name, please try again{reset}\n")
        start()
    cursor.execute(sql_start_patient)
    cursor.execute(sql_start_quiz)
    cursor.execute(sql_start_used)

    return screen_name


def pause():
    input('Press enter to continue your mission...\n')
    return


def quiz_randomizer():
    quizlista = []

    sql_quiz = f"SELECT id FROM airport"
    cursor = yhteys.cursor()
    cursor.execute(sql_quiz)
    res_quiz = cursor.fetchall()

    while len(quizlista) < 6:
        m = random.randint(2, 21)
        if m not in quizlista:
            quizlista.append(m)

    for i in range(cursor.rowcount):
        if res_quiz[i][0] in quizlista:
            sql_quiz_update = (f"UPDATE airport SET quiz = 1 WHERE id = '{res_quiz[i][0]}'")
            kursori = yhteys.cursor()
            kursori.execute(sql_quiz_update)

    return


def game_start():
    # Pelaaja valitsee, haluaako valita pelin
    # Loop jatkuu, kunnes pelaaja antaa vastaukseksi joko Y (kyllä) tai N (ei)
    intro()

    valid_input = False

    while not valid_input:
        game_input = input("Would you like to start a new game? (y/n): ").upper()

        if game_input == "Y" or game_input == "N":
            valid_input = True

        else:
            print(f"\n{red}Invalid input, please try again{reset}\n")
            continue

    return game_input


def backlore():
    valid_input = False

    while not valid_input:

        backlore = input('\nWould you like to read the backlore? (y/n): ').upper()

        if backlore == "Y":
            valid_input = True
            lore()
        elif backlore == "N":
            valid_input = True
        else:
            print(f"\n{red}Invalid input, please try again{reset}")
            continue
    return


def player_coord():
    # pelaajan sijainnin koordinaatit
    sql_player_coord = (f"SELECT latitude_deg, longitude_deg FROM airport "
                        f"INNER JOIN player ON airport.ident = player.location;")

    cursor = yhteys.cursor()
    cursor.execute(sql_player_coord)
    res_player_coord = cursor.fetchall()
    return res_player_coord


def distances():
    # ohjelma hakee kaikkien lentokenttien koordinaatit (pl. pelaajan sijainti)
    sql_airport_coord = (f"SELECT latitude_deg, longitude_deg FROM airport"
                         f" WHERE ident NOT IN (SELECT location FROM player) AND ident != 'ENTR'")

    cursor = yhteys.cursor()
    cursor.execute(sql_airport_coord)
    res_airport_coord = cursor.fetchall()

    # ohjelma hakee kaikkien lentokenttien kunnat ja icao-koodit
    sql_municipality = (f"SELECT municipality from airport"
                        f" where ident not in (select location from player) AND ident != 'ENTR'")

    cursor.execute(sql_municipality)
    res_municipality = cursor.fetchall()

    # ohjelma hakee kaikkien lentokenttien kunnat ja icao-koodit
    sql_icao = (f"SELECT ident from airport"
                f" where ident not in (select location from player) AND ident != 'ENTR'")

    cursor.execute(sql_icao)
    res_icao = cursor.fetchall()

    # ohjelma kertoo pelaajan jäljellä olevan rangen

    # vertailu muihin kuntiin kuin kotisairaalaan
    # mikäli range riittää toiseen kuntaan, ohjelma lisää listaan kunnan ja lopuksi lista tulostetaan

    lista = []

    if goal() < 9:
        for i in range(cursor.rowcount):
            comparison = int(distance.distance({player_coord()[0]}, {res_airport_coord[i]}).km)

            if comparison <= int(float(player_range())):
                lista.append([res_municipality[i][0], res_icao[i][0], comparison])

        # Format the table with tabulate
        table = tabulate(lista, headers=['Location', 'ICAO', 'Distance(km)'], tablefmt="fancy_grid")

        # Add color to the table using termcolor
        styled_table = colored(table, "blue")

    elif goal() >= 9:
        for i in range(cursor.rowcount):
            comparison = int(distance.distance({player_coord()[0]}, {res_airport_coord[i]}).km)
            comparison = int(comparison * 1.2)

            if int(comparison) <= int(float(player_range())):
                lista.append([res_municipality[i][0], res_icao[i][0], comparison])

        # Listan muotoilu selkeäksi taulukoksi
        table = tabulate(lista, headers=['Location', 'ICAO', 'Distance(km)'], tablefmt="fancy_grid")
        # Lisätää
        # styled_table = colored(table, "blue")

    if len(lista) > 0:
        print(f"\nThese locations are within your range:")
        print(table)
    elif len(lista) == 0:
        print(f"No location is within your range.")
    return lista


def helicopter():
    # hakee helikopterissa olevien potilaiden määrän
    sql_heli = "SELECT patient_qty FROM player"
    cursor = yhteys.cursor()
    cursor.execute(sql_heli)
    res_heli = cursor.fetchone()
    return res_heli[0]


# vertailu kotisairaalaan
def home_hospital():
    sql_home_coord = (f"SELECT latitude_deg, longitude_deg from airport"
                      f" where ident = 'ENTR'")

    cursor = yhteys.cursor()
    cursor.execute(sql_home_coord)
    res_home_coord = cursor.fetchall()

    # ohjelma kertoo jos pelaaja on kotisairaalassa tai mikä olisi etäisyys sinne
    comparison_home = int(distance.distance({player_coord()[0]}, {res_home_coord[0]}).km)

    if comparison_home == 0:
        colored_text(f"{underline}\nYou are at the home hospital: Trondheim (ENTR){reset}", green,)

    # elif helicopter() == 0:
    #    print(f"\nYour distance to the home hospital (ENTR) is {comparison_home} kilometers, \n"
    #          f"but you can't go home without any rescued patients")

    else:
        print(f"\n{underline}Your distance to the home hospital {green}(Trondheim, ENTR){reset}{underline} is {green}{comparison_home}{reset}{underline} kilometers{reset}")

    return


# hakee pelaajan sen hetkisen rangen
def player_range():
    sql_range = f"SELECT range_km from player"

    cursor = yhteys.cursor()
    cursor.execute(sql_range)
    res_range = cursor.fetchone()

    return res_range[0]


# pelaaja valitsee mihin haluaa siirtyä seuraavaksi
def destination():
    markdown(f"Your range is {green}{player_range()}{reset} kilometers ", reset)
    valid_input = False

    # Valinta-loop pyörii niin kauan, että pelaaja syöttää oikean ICAO-koodin

    while not valid_input:
        new_location = input_field('Choose your destination',
                                   'Type an ICAO code from the list below to fly there\nor type "map" to open the map of Norway.').upper()
        sql_icao_coord = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{new_location}'"

        # Suorittaa sql-komennon
        try:
            cursor = yhteys.cursor()
            cursor.execute(sql_icao_coord)
            res_icao_coord = cursor.fetchall()

            if new_location == "MAP":
                norway_map()
                valid_input = False
                home_hospital()  # Pelaajan ja kotisairaalan etäisyys:
                patient_icao(patient_locations, patient_municipalities)  # Tulostetaan potilaiden sijainnit
                # Pelastettujen potilaiden kokonaistilanne näytetään pelaajalle aina kotisairaalassa

                if player_location()[0] == 'ENTR':
                    markdown(f"{bold}{goal()}{reset} out of {bold}12{reset} patients rescued to the hospital", reset)

                markdown(f"Your range is {green}{player_range()}{reset} kilometers ", reset)

            elif cursor.rowcount == 0:
                print(f"{warning}Location not found, try again{reset}\n")
                valid_input = False

            elif cursor.rowcount >= 1:
                valid_input = True

        # Estää ohjelman kaatumisen virheellisen syötteen vuoksi
        except mysql.connector.errors.ProgrammingError:
            print(f"{warning}Location not found, try again{reset}\n")
            valid_input = False

    # Lasketaan, riittääkö range halutulle lentokentälle
    if cursor.rowcount > 0:
        destination_distance = int(distance.distance(player_coord(), res_icao_coord).km)

        if destination_distance <= int(player_range()):

            if new_location == player_location()[0]:
                print(f'\n{warning}You are already at {new_location}, please try again{reset}\n')
                destination()

            # elif new_location == 'ENTR' and helicopter() == 0:
            #    print('\nYou cannot return to home with empty helicopter, please try again')
            #    destination()

            else:
                sql_update_location = (f"UPDATE player SET location = '{new_location}'")
                sql_select_location = (f"SELECT municipality, ident FROM airport WHERE ident = '{new_location}'")
                cursor = yhteys.cursor()
                cursor.execute(sql_update_location)
                cursor.execute(sql_select_location)
                res_select_location = cursor.fetchone()
                print(f"\n{green}You have arrived at {res_select_location[0]} ({res_select_location[1]}), welcome!{reset}")

                if goal() < 9:
                    old_range = int(player_range())
                    new_range = old_range - destination_distance
                    sql_new_range = (f"UPDATE player SET range_km = '{new_range}'")
                    cursor = yhteys.cursor()
                    cursor.execute(sql_new_range)

                elif goal() >= 9:
                    old_range = int(player_range())
                    new_range = int(old_range - destination_distance * 1.2)
                    sql_new_range = (f"UPDATE player SET range_km = '{new_range}'")
                    cursor = yhteys.cursor()
                    cursor.execute(sql_new_range)


        elif destination_distance > int(player_range()):
            print(f"{warning}You don't have enough range to travel to this destination ")
            destination()

    # if cursor.rowcount == 0 :
    #     print(f"Please try again")
    #     destination()
    return


# quiz game
def quiz():
    randomizing = True

    print(f"\n{cyan}{bold}{underline}QUIZ GAME{reset}\nThere happens to be quiz game on your location! "
          f"\nThe questions are Norway related\n\nThe rules are quite simple:"
          f"\nRight answer you gain {green}300km{reset} amount of range \nWrong answer you lose {green}150km{reset} amount of range                 ")

    # etsii kysymyksen, jota ei oel vielä käytetty
    while randomizing:
        m = random.randint(1, 8)

        sql_question = f"SELECT question, option1, option2, option3, correct FROM quiz WHERE id = '{m}' and used = 0"
        cursor = yhteys.cursor()
        cursor.execute(sql_question)
        res_question = cursor.fetchone()
        if cursor.rowcount == 0:
            randomizing = True
        else:
            randomizing = False

    # muuttujat sql-haun tuloksille
    question = res_question[0]
    a = res_question[1]
    b = res_question[2]
    c = res_question[3]
    correct_answer = res_question[4]

    # quiz game loop

    played = False
    answered = False

    while not played:

        # pelaaja päättää haluaako vastata quiz game -kysymykseen

        quiz_input = (input("\nWould you like to play? y/n : ")).upper()

        # pelaaja päättää pelata

        if quiz_input == "Y":

            sql_quiz_used = f"UPDATE quiz SET used = 1 WHERE id = '{m}'"
            sql_quiz_update = f"UPDATE airport SET quiz = 0 WHERE ident = '{player_location()[0]}'"
            cursor.execute(sql_quiz_used)
            cursor.execute(sql_quiz_update)

            print(f"\n{green}{underline}Welcome to play a quiz game!\n{reset}")

            print(f"{question}"
                  f"\n{bold}{cyan}a){reset} {a} or {bold}{cyan}b){reset} {b} or {bold}{cyan}c){reset} {c}")

            # pelaaja vastaa oikein
            while not answered:

                played = True
                answer = input("\nEnter your answer: ").lower()

                if answer not in ("a", "b", "c"):
                    print(f"{red}Invalid input, please try again{reset}\n")

                    answered = False

                elif answer == correct_answer:

                    sql_quiz_fuel = f"UPDATE player SET range_km = range_km + 300"
                    cursor.execute(sql_quiz_fuel)
                    print(f"\nYour answer - {correct_answer} - {green}is right!{reset}"
                          f"\nYou gained {green}300km{reset} amount of range and your new range is {green}{player_range()}{reset} kilometers\n")

                    answered = True


                # pelaaja vastaa väärin
                # peli saattaa päättyä tähän, koska väärä vastaus vähentää rangea

                elif answer != correct_answer:

                    sql_quiz_fuel = f"UPDATE player SET range_km = range_km - 150"
                    cursor.execute(sql_quiz_fuel)
                    print(f"\n{red}Your answer was wrong{reset}"
                          f"\nThe right answer was {green}{correct_answer}{reset}")

                    if int(player_range()) > 0:
                        print(f"\nYou just lost {green}150km{reset} amount of range and "
                              f"your new range is {green}{player_range()}{reset} kilometers\n")

                    elif int(player_range()) <= 0:
                        print(f"\nYou just lost {green}150km{reset} amount of range and "
                              f"ran out of range\n")

                    answered = True
                    break

        # pelaaja kieltäytyy pelaamasta

        elif quiz_input == "N":

            print(f"{warning}Your choice, but you'll be missed. Please, continue your journey.\n{reset}")
            break

        # syötetty vastaus on virheellinen ja vastaus kysytään uudelleen

        else:
            print(f"{red}Wrong input, try again!{reset}")
            continue

    return


# potilaiden sijaintien arpominen
def patient_location():
    icaolista = []

    while len(icaolista) < 12:
        m = random.randint(2, 21)
        if m not in icaolista:
            icaolista.append(m)

    for i in range(12):
        uus = icaolista[i]
        sql = (f"UPDATE patient SET location = (SELECT ident FROM airport WHERE airport.id = '{uus}') "
               f"WHERE patient.id = '{i + 1}'")
        kursori = yhteys.cursor()
        kursori.execute(sql)

    return


def acute_randomizer():
    cursor = yhteys.cursor()

    sql_acute = (f"SELECT location FROM patient ORDER BY RAND(1) LIMIT 1;")
    cursor.execute(sql_acute)
    res_acute = cursor.fetchone()
    return res_acute


# arpoo 3 potilaan tiedot, joita ei ole vielä pelastettu
def patient_randomizer(acute_location):
    patient_list = []
    cursor = yhteys.cursor()
    while len(patient_list) < 3:

        patient_no = random.randint(1, 12)
        if goal() < 3:
            sql_patient_no = (f"SELECT location FROM patient WHERE id = '{patient_no}' AND rescued = 0 "
                              f"AND location != '{acute_location[0]}'")
        elif goal() >= 3:
            sql_patient_no = (f"SELECT location FROM patient WHERE id = '{patient_no}' AND rescued = 0")

        cursor.execute(sql_patient_no)
        res_patient_no = cursor.fetchone()

        if res_patient_no is not None:
            if res_patient_no[0] not in patient_list:
                patient_list.append(res_patient_no[0])

    return patient_list

def patient_municipality(patient_list):

    # kokoaa dictionaryn, jossa näkyy jäljellä olevien potilaiden sijainnin icao ja nimi

    patient_list_mun = {}

    sql_patient_mun = (f"SELECT ident, municipality FROM airport")
    cursor = yhteys.cursor()
    cursor.execute(sql_patient_mun)
    res_patient_mun = cursor.fetchall()

    for i in range(cursor.rowcount):
        if res_patient_mun[i][0] in patient_list:
            patient_list_mun.update({res_patient_mun[i][0]: res_patient_mun[i][1]})

    return patient_list_mun

def patient_icao(patient_list, patient_list_mun):

    # tulostaa jäljellä olevien pelastettavien potilaiden sijainnit

    sql_patient_icao = f"SELECT location FROM patient WHERE rescued = 1"
    cursor = yhteys.cursor()
    cursor.execute(sql_patient_icao)
    res_patient_icao = cursor.fetchall()

    # poistaa jäljellä olevien potilaiden listasta jo haetut

    for i in range(cursor.rowcount):
        if res_patient_icao[i][0] in patient_list and res_patient_icao[i][0] in patient_list_mun:
            patient_list_mun.pop(res_patient_icao[i][0])

    # tulostaa jäljellä olevien potilaiden listan
    # kehottaa palaamaan kotiin, jos kaikki potilaat on jo haettu

    separate = ' • '
    result = separate.join(str(value) + f"{green} (" + str(key) + f"){reset}" for key, value in patient_list_mun.items())

    if len(patient_list) > 0:
        if len(patient_list_mun) > 1:
            # markdown(f"Patients are located at \n  {result}\n", reset)
            print(f"Patients are located at \n  {result}\n")

        elif len(patient_list_mun) == 1:
            # markdown(f"Patient is located at \n  {result}\n", reset)
            print(f"Patient is located at \n  {result}\n")

    elif len(patient_list) == 0 and player_location()[0] != "ENTR":
        markdown(f"No patients to be saved this time - return to home to get new patient list", warning)

    return


# hakee pelaajan sijainnin
def player_location():
    sql_rescue_player = f"SELECT location FROM player"
    cursor = yhteys.cursor()
    cursor.execute(sql_rescue_player)
    res_rescue_player = cursor.fetchone()
    return res_rescue_player


# tarkistetaan onko pelaajan sijainnissa potilasta, jota ei ole vielä pelastettu
def rescue_patient(patient_list):
    cursor = yhteys.cursor()
    res_rescue_player = player_location()

    if res_rescue_player is not None:

        player_loc = res_rescue_player[0]

        if player_loc in patient_list:
            sql_rescue_patient = f"SELECT id FROM patient WHERE rescued = 0 AND location = '{player_loc}'"
            cursor = yhteys.cursor()
            cursor.execute(sql_rescue_patient)
            res_rescue_patient = cursor.fetchone()

            update_rescue_patient = f"UPDATE patient SET rescued = 1 WHERE id = '{res_rescue_patient[0]}'"
            update_patient_qty = f"UPDATE player SET patient_qty = (patient_qty + 1) where id = 1"
            cursor.execute(update_patient_qty)
            cursor.execute(update_rescue_patient)

            if cursor.rowcount != 0:
                if player_location()[0] == acute_randomizer()[0]:
                    if helicopter() == 0:
                        print(f"\nYou saved 3 patients from avalanche")
                    elif helicopter() == 1:
                        print(f"\nYou saved 2 patients from avalanche")
                    elif helicopter() == 2:
                        print(f"\nYou saved 1 patient from avalanche")

                    print(f"\nDue to the acute avalanche situation in the mountains, \n"
                          f"you flew directly back to the home hospital.\n"
                          f"{green}The avalanche victims are now safe, thanks to you, hero!{reset}\n")
                    update_player_home = f"UPDATE player SET location = 'ENTR' where id = 1"
                    cursor.execute(update_player_home)
                elif player_location()[0] != acute_randomizer()[0]:
                    print(f"{green}You have picked up one of your patients.{reset}\n")


        else:

            if player_location()[0] != 'ENTR':
                print(f"{green}There is no patient to be saved here.{reset}\n")

    # Tarkistetaan onko pelaajan sijainnissa quiz game

    sql_quiz_query = (f"SELECT quiz FROM airport WHERE ident = '{player_location()[0]}'")
    cursor.execute(sql_quiz_query)
    res_quiz_query = cursor.fetchone()

    if res_quiz_query[0] == 1:
        quiz()

    return


# tarkistetaan onko pelaaja saavuttanut pelin tavoitteen
def goal():
    sql_victory = "SELECT patient_goal FROM player WHERE id = 1"
    cursor = yhteys.cursor()
    cursor.execute(sql_victory)
    res_victory = cursor.fetchone()
    res_victory = res_victory[0]
    return res_victory


# päivittää pelaajan tietoja kotisairaalassa
# range lisääntyy vain, mikäli pelaaja vie sairaalaan myös potilaita
def update_goal():
    if helicopter() == 3:
        sql_goal = "UPDATE player SET range_km = range_km + 500, patient_goal = patient_goal + patient_qty, patient_qty = 0 WHERE location = 'ENTR'"
        cursor = yhteys.cursor()
        cursor.execute(sql_goal)
        print(f"You gained {green}500km{reset} of range because you rescued the patients!\n")
        pause()

    elif helicopter() < 3:
        sql_goal = "UPDATE player SET patient_goal = patient_goal + patient_qty, patient_qty = 0 WHERE location = 'ENTR'"
        cursor = yhteys.cursor()
        cursor.execute(sql_goal)
    return


def patient_aku():
    boolean = True

    while boolean == True:
        m = random.randint(1, 12)
        sql_patient_loc = f"SELECT location FROM patient WHERE rescued = 0 AND id = '{m}'"
        cursor = yhteys.cursor()
        cursor.execute(sql_patient_loc)
        res_patient_loc = cursor.fetchone()
        if cursor.rowcount == 0:
            boolean = True
        else:
            boolean = False

    return res_patient_loc


def final_boss():
    answered = False
    dialogue_print_before()


    print(f'{underline}The patient is having an asthma attack, what is your next move?{reset}')

    while not answered:
        answer = input(f'{cyan}a){reset} Give her something to eat {cyan}b){reset} Give her a hug {cyan}c){reset} Help her to use the inhaler'
                       '\n\nChoose your next move: ').upper()

        if answer not in ('A', 'B', 'C'):
            answered = False
            print(f"{red}Invalid input, please try again{reset}\n")
            continue

        elif answer == "C":
            print('')
            dialogue_print_after()
            answered = True
            game_end = "win"

        elif answer == 'A' or answer == 'B':
            print(f"\nBecause of your next move unfornutaly your patient didn't survive.")
            answered = True
            game_end = "lose"

    return game_end


# PELIN ALOITUS


# Pelaaja valitsee, tahtooko aloittaa uuden pelin
new_game = game_start()

if new_game == "N":
    colored_text(f"Oh no! You missed on a life-changing mission! ", warning)

if new_game == "Y":
    colored_text(f"Congratulations! You're about to start a rescue mission.", green)

    # Pelaaja valitsee, haluaako lukea taustatarinan
    backlore()
    screen_name = start()  # resetoi tietokannan peliä varten

    # Säännöt pelaajalle
    cool_field('Game rules', f"\nSave all the patients from different cities and return them to the home hospital."
                             f"\nFor every round you gain more range to save more patients."
                             f"\n\nThe helicopter has a maximum capacity of 3 patients."
                             f"\n\nThe game also contains quiz games, where you have a chance to gain more range."
                             f"\n\nThe game ends when you have saved all the patients or you ran out of range.")

    # Meidän easter egg hihi
    if screen_name.upper() == 'TINJA':
        embark = 'embark'
        starting = input(f'Press Enter to {cyan}{embark}{reset} on your journey, {screen_name}...')
    else:
        starting = input(f'Press Enter to start on your journey, {cyan}{screen_name}...{reset}\n')

    quiz_randomizer()  # arpoo quiz-minipelien sijainnit
    patient_location()  # arpoo potilaiden sijainnit
    acute_location = acute_randomizer()  # arpoo akuuttitapauksen sijainnin
    patient_locations = patient_randomizer(acute_location)  # arpoo ensimmäiset 3 pelastettavaa potilasta
    patient_municipalities = patient_municipality(patient_locations)

    # Boolean
    game_over = False
    win = False

    while not game_over and not win:

        patient_goal = goal()

        rescue_patient(patient_locations)

        # pelaajan tiedot päivittyvät kotisairaalassa
        if player_location()[0] == 'ENTR':
            update_goal()

        # game loop päättyy kun pelaaja saa pelitavoitteen täyteen
        if goal() >= 12:

            if final_boss() == "win":
                win = True
            else:
                game_over = True

        # game loop jatkuu jos pelitavoite ei ole täynnä
        elif goal() < 12:

            # Pause-funktio pyytää pelaajaa painamaan enteriä jatkaakseen
            # Estämään liian pitkää tekstiä terminalissa kerralla
            if player_location()[0] != 'ENTR':
                pause()

            # Tulostaa etäisyydet eri sijainteihin
            distance_lista = distances()

            # Peli päättyy jos range ei riitä yhteenkään locationiin
            if len(distance_lista) == 0:
                game_over = True

            # Peli jatkuu, jos range riittää väh. 1 sijaintiin
            else:

                # Kertoo pelaajalle helikopterin potilastilanteen, mikäli ei ole kotisairaalassa (ENTR)

                if player_location()[0] != 'ENTR':
                    if helicopter() < 1:
                        print(f"{warning}You don't have any patients in the helicopter and you still have space for 3 patients{reset}")

                    if 1 <= helicopter() < 3:
                        print(f"{warning}Patients picked up: {helicopter()} - still space for {3 - helicopter()} more patients{reset}")

                    if helicopter() == 3:
                        print(f"{warning}Patient picked up: {helicopter()} - helicopter is full "
                              f"and you have to return to the home hospital{reset}")

                home_hospital()  # Pelaajan ja kotisairaalan etäisyys:

                patient_icao(patient_locations, patient_municipalities)  # Tulostetaan potilaiden sijainnit

                # Pelastettujen potilaiden kokonaistilanne näytetään pelaajalle aina kotisairaalassa

                if player_location()[0] == 'ENTR':
                    markdown(f"{bold}{goal()}{reset} out of {bold}12{reset} patients rescued to the hospital", reset)

                if goal() in (3, 6, 9):

                    # print(f"In total {goal()}/12 patients rescued to the hospital")

                    # Peli vaikeutuu, kun 75% potilaista on viety sairaalaan

                    if goal() >= 9:
                        print(f"\nOh no! The weather in the mountains has got really awful. \n"
                              f"The helicopter uses now 20% more fuel due to strong headwind.\n")

                    # Pelaaja saa uudet 3 kohdetta, kun kaikki 3 edellistä on käyty ja viety sairaalaan

                    if player_location()[0] == 'ENTR':
                        patient_locations = patient_randomizer(acute_location)  # Arpoo 3 potilasta
                        patient_municipalities = patient_municipality(patient_locations)
                        patient_icao(patient_locations, patient_municipalities)  # Tulostaa potilastlistan

                    destination()

                else:

                    destination()  # mahdolliset kohteet, mihin pelaaja tahtoo mennä

    # Voitto

    if win == True:
        print(
            f"{green}Congratulations!{reset} You have completed the game. "
            f"\nYou have saved all the patients and you are hailed as the {green}{bold}{underline}hero{reset} of Norway.")

        hero_of_norway = """
                 _______________
                |@@@@|     |####|
                |@@@@|     |####|
                |@@@@|     |####|
                \@@@@|     |####/
                 \@@@|     |###/
                  `@@|_____|##'
                       (O)
                    .-'''''-.
                  .'  * * *  `.
                 :  *       *  :
                : Hero of Norway :
                : ~ A W A R D ~ :
                 :  *       *  :
                  `.  * * *  .'
                    `-.....-'
                    """

        print(green + hero_of_norway)

    # Gameover

    if game_over == True:
        print(f"{red}Game over. Unfortunately, you weren't able to save all the 12 patients this time :(")
