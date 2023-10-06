import random
import mysql.connector
from geopy import distance
from tabulate import tabulate

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='ronistrom',
    autocommit=True
)


# FUNKTIOT


def start():
    screen_name = input("\nWhat's your name? ")
    sql_start = (f"UPDATE player SET screen_name = '{screen_name}', "
                 f"location = 'ENTR', patient_goal = 0, patient_qty = 0, "
                 f"range_km = 10000 WHERE id = 1")
    sql_start_patient = f"UPDATE patient SET rescued = 0"

    cursor = yhteys.cursor()
    cursor.execute(sql_start)
    cursor.execute(sql_start_patient)
    return

def game_start():
    # Pelaaja valitsee, haluaako valita pelin
    # Loop jatkuu, kunnes pelaaja antaa vastaukseksi joko Y (kyllä) tai N (ei)

    valid_input = False

    while not valid_input:
        game_input = input("Would you like to start a game? (y/n): ").upper()

        if game_input == "Y" or game_input == "N":
            valid_input = True

        else:
            print(f"\nInvalid input, please try again:")
            continue

    return game_input
def lore():
    print(f"Medihelipeli: A Race Against Time \nTime is running out. "
          f"Equipped with an advanced emergency rescue helicopter No. 330 Squadron RNoAF, \nyou are set on a dangerous patient saving journey "
          f"in the beautiful landscape of Norway. \nYour helicopter's fuel is limited, and each rescue mission consumes a significant portion of it. "
          f"The goal is to save all twelve patients before you run out of fuel. "
          f"\nEach rescue attempt must be carefully calculated to maximize fuel efficiency while minimizing the time taken to reach and rescue the patients. "
          f"\nThere are three kinds of danger levels (1-3). The level depends on the severity of the patient's injury. "
          f"Depending on the severity of the injury, the level changes. \nIf you manage to save all twelve patients within the fuel constraints, "
          f"you're hailed as a hero, and the skies of Norway echo with the stories of your courage. \nHowever if your fuel runs out before completing the rescue missions, "
          f"your journey ends, and the fate of the remaining patients remains uncertain.")
    return


def player_coord():
    # pelaajan sijainnin koordinaatit
    sql_player_coord = (f"SELECT latitude_deg, longitude_deg from airport"
                        f" where ident in (select location from player)")

    cursor = yhteys.cursor()
    cursor.execute(sql_player_coord)
    res_player_coord = cursor.fetchall()
    return res_player_coord


def distances():
    # ohjelma hakee kaikkien lentokenttien koordinaatit (pl. pelaajan sijainti)
    sql_airport_coord = (f"SELECT latitude_deg, longitude_deg from airport"
                        f" where ident not in (select location from player) AND ident != 'ENTR'")

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
    for i in range(cursor.rowcount):
        comparison = int(distance.distance({player_coord()[0]}, {res_airport_coord[i]}).km)

        if comparison <= float(player_range()[0]):
            lista.append([res_municipality[i][0], res_icao[i][0], comparison])

    if len(lista) > 0:
        print(f"\nThese locations are within your range:")
        print(tabulate(lista, headers=['Location', 'ICAO', 'Distance(km)']))
    elif len(lista) == 0:
        print(f"No location is within your range.")
    return lista

def helicopter():
    # hakee helikopterissa olevien potilaiden määrän
    sql_heli = "SELECT patient_qty FROM player"
    cursor = yhteys.cursor()
    cursor.execute(sql_heli)
    res_heli = cursor.fetchone()
    res_heli = res_heli[0]
    return res_heli

def home_hospital():
    # vertailu kotisairaalaan
    sql_home_coord = (f"SELECT latitude_deg, longitude_deg from airport"
                        f" where ident = 'ENTR'")

    cursor = yhteys.cursor()
    cursor.execute(sql_home_coord)
    res_home_coord = cursor.fetchall()

    # ohjelma kertoo jos pelaaja on kotisairaalassa tai mikä olisi etäisyys sinne
    comparison_home = int(distance.distance({player_coord()[0]}, {res_home_coord[0]}).km)
    if comparison_home == 0:
        print(f"\nYou are at the home hospital")
    elif helicopter() == 0:
        print(f"\nYour distance to the home hospital (ENTR) is {comparison_home} kilometers, \nbut you can't go home without any rescued patients")

    else:
        print(f"\nYour distance to the home hospital (ENTR) is {comparison_home} kilometers")
    return

# hakee pelaajan sen hetkisen rangen
def player_range():
    sql_range = f"SELECT range_km from player"

    cursor = yhteys.cursor()
    cursor.execute(sql_range)
    res_range = cursor.fetchone()
    return res_range

# pelaaja valitsee mihin haluaa siirtyä seuraavaksi
def destination():
    print(f"Your range is {player_range()[0]} kilometers ")
    new_location = input('Type the ICAO code: ').upper()
    sql_icao_coord = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{new_location}'"
    try:
        cursor = yhteys.cursor()
        cursor.execute(sql_icao_coord)
        res_icao_coord = cursor.fetchall()
    except mysql.connector.errors.ProgrammingError:
        print(f"Location not found, try again")
        destination()

    # Lasketaan, riittääkö range halutulle lentokentälle
    if cursor.rowcount > 0:
        destination_distance = int(distance.distance(player_coord(), res_icao_coord).km)
        if destination_distance <= int(player_range()[0]):
            if new_location == player_location()[0]:
                print(f'\nYou are already at {new_location}, please try again')
                destination()
            elif new_location == 'ENTR' and helicopter() == 0:
                print('\nYou cannot return to home with empty helicopter, please try again')
                destination()
            else:
                sql_update_location = (f"UPDATE player SET location = '{new_location}'")
                cursor = yhteys.cursor()
                cursor.execute(sql_update_location)
                print(f"\nYou are now at {new_location}")

                # Päivitetään uusi range
                old_range = int(player_range()[0])
                new_range = old_range - destination_distance
                sql_new_range = (f"UPDATE player SET range_km = '{new_range}'")
                cursor = yhteys.cursor()
                cursor.execute(sql_new_range)
        elif destination_distance > int(player_range()[0]):
            print(f"You don't have enough range to travel to this destination ")
            destination()

    if cursor.rowcount == 0:
        print(f"Please try again")
        destination()
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

# arpoo 3 potilaan tiedot, joita ei ole vielä pelastettu
def patient_randomizer():
    patient_list = []
    while len(patient_list) < 3:
        patient_no = random.randint(1, 12)
        sql_patient_no = f"SELECT location FROM patient WHERE id = '{patient_no}' AND rescued = 0"
        cursor = yhteys.cursor()
        cursor.execute(sql_patient_no)
        res_patient_no = cursor.fetchone()
        if res_patient_no is not None:
            if res_patient_no[0] not in patient_list:
                patient_list.append(res_patient_no[0])

    return patient_list

# tulostaa jäljellä olevien pelastettavien potilaiden sijainnit
def patient_icao(patient_list):
    sql_patient_icao = f"SELECT location FROM patient WHERE rescued = 1"
    cursor = yhteys.cursor()
    cursor.execute(sql_patient_icao)
    res_patient_icao = cursor.fetchall()

    for i in range(cursor.rowcount):
        if res_patient_icao[i][0] in patient_list:
            patient_list.remove(res_patient_icao[i][0])
    if len(patient_list) == 3:
        print(f"Patients are located at {patient_list[0]}, {patient_list[1]} and {patient_list[2]}")
    elif len(patient_list) == 2:
        print(f"Patients are located at {patient_list[0]} and {patient_list[1]}")
    elif len(patient_list) == 1:
        print(f"Last patient to be saved is located at {patient_list[0]}")
    elif len(patient_list) == 0 and player_location()[0] != "ENTR":
        print(f"No patients to be saved this time - return to home to get new patient list")
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
    res_rescue_player = player_location()
    if res_rescue_player is not None:
        player_loc = res_rescue_player[0]
        if player_loc in patient_list:
            sql_rescue_patient = f"SELECT id FROM patient WHERE rescued = 0 AND location = '{player_loc}'"
            cursor = yhteys.cursor()
            cursor.execute(sql_rescue_patient)
            res_rescue_patient = cursor.fetchall()

            if cursor.rowcount != 0:
                print(f"You have picked up one of your patients.")
                update_rescue_patient = f"UPDATE patient SET rescued = 1 WHERE id = '{res_rescue_patient[0][0]}'"
                update_patient_qty = f"UPDATE player SET patient_qty = (patient_qty + 1) where id = 1"
                cursor.execute(update_patient_qty)
                cursor.execute(update_rescue_patient)
        else:
            if player_location()[0] != 'ENTR':
                print(f"There is no patient to be saved here.")
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
def update_goal():
    sql_goal = "UPDATE player SET range_km = range_km + 500, patient_goal = patient_goal + patient_qty, patient_qty = 0 WHERE location = 'ENTR'"
    cursor = yhteys.cursor()
    cursor.execute(sql_goal)
    return

# PELIN ALOITUS


# Pelaaja valitsee, tahtooko aloittaa uuden pelin
new_game = game_start()

if new_game == "N":
    print(f"Oh no! You missed on a life-changing mission! ")

if new_game == "Y":
    print(f"Congratulations! You're about to start a rescue mission.")



    # Backlore
    backlore = input('\nWould you like to read the backlore? y/n: ').upper()
    if backlore == "Y":
        lore()

    # säännöt pelaajalle
    print('Game goal: save the patients and return them to the home hospital')


    start() #resetoi tietokannan peliä varten
    patient_location() # arpoo potilaiden sijainnit
    patient_locations = patient_randomizer()


# GAME LOOP


    game_over = False
    win = False

    while not game_over and not win:
        patient_goal = goal()
        if patient_goal != 12:
            rescue_patient(patient_locations)
            jatka = input('Press enter to continue your mission...')
            distance_lista = distances()

            if len(distance_lista) == 0:
                game_over = True
            else:

                # kertoo pelaajalle helikopterin potilastilanteen
                if player_location()[0] != 'ENTR':
                    if helicopter() < 1:
                        print(f"You don't have any patients in the helicopter and you still have space for 3 patients")

                    if 1 <= helicopter() < 3:
                        print(f"Patients picked up: {helicopter()} - still space for {3 - helicopter()} more patients")

                    if helicopter() == 3:
                        print(f"Patient picked up: {helicopter()} - helicopter is full "
                            f"and you have to return to the home hospital")



                home_hospital()  # pelaajan ja kotisairaalan etäisyys:
                patient_icao(patient_locations) # tulostetaan potilaiden sijainnit
                if player_location()[0] == 'ENTR' and helicopter() != 0:
                    update_goal()
                print(f"Saved patients {goal()}")  # kuinka monta potilasta on saatu sairaalaan
                if goal() in (3, 6, 9):
                    print(f"{goal()} patients saved")
                    if player_location()[0] == 'ENTR':
                        patient_locations = patient_randomizer()  # arpoo 3 potilasta
                        patient_icao(patient_locations)
                    destination()
                else:
                    destination()  # mahdolliset kohteet, mihin pelaaja tahtoo mennä

        if patient_goal == 12:
            print("Congratulations! You have completed the game. \nYou have saved all the patients and you are hailed as the hero of Norway.")
            win = True

    if game_over == True:
        print(f"Game over. You are out of range. :(")
