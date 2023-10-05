import random
import mysql.connector
from geopy import distance
from tabulate import tabulate

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='KierukkaKupariNöö7!',
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
    print(f'*backlore will be here*')
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
    print(f"Your current range is {player_range()[0]} kilometers")

    # vertailu muihin kuntiin kuin kotisairaalaan
    # mikäli range riittää toiseen kuntaan, ohjelma tulostaa kunnan nimen ja heliportin icao-koodin

    lista = []
    for i in range(cursor.rowcount):
        comparison = int(distance.distance({player_coord()[0]}, {res_airport_coord[i]}).km)

        if comparison <= float(player_range()[0]):
            lista.append([res_municipality[i][0], res_icao[i][0], comparison])

            # print(f"{res_municipality[i][0]} - {res_icao[i][0]} - {comparison}")

    if len(lista) > 0:
        print(f"\nThese locations are within your range:")
        print(tabulate(lista, headers=['Location', 'ICAO', 'Distance(km)']))
    elif len(lista) == 0:
        print(f"No location is within your range.")
    return lista

def helicopter():
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
        print("You can't go home!")

    else:
        print(f"\nYour distance to the home hospital (ENTR) is {comparison_home} kilometers")
    return


def player_range():
    # hakee pelaajan sen hetkisen rangen
    sql_range = f"SELECT range_km from player"

    cursor = yhteys.cursor()
    cursor.execute(sql_range)
    res_range = cursor.fetchone()
    return res_range


def destination():  # kohde minne haluat matkustaa
    new_location = input('Type the ICAO code: ').upper()
    sql_icao_coord = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{new_location}'"
    cursor = yhteys.cursor()
    cursor.execute(sql_icao_coord)
    res_icao_coord = cursor.fetchall()

    # Lasketaan, riittääkö range halutulle lentokentälle
    if cursor.rowcount > 0:
        destination_distance = int(distance.distance(player_coord(), res_icao_coord).km)
        if destination_distance <= int(player_range()[0]):
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
            print(f"Your new range is {new_range} kilometers ")
        elif destination_distance > int(player_range()[0]):
            print(f"You don't have enough range to travel to this destination ")
            destination()

    if cursor.rowcount == 0:
        print(f"Please try again")
        destination()
    return


# patient location arpominen
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


def patient_randomizer():
    # arpoo 3 potilaan tiedot, joita ei ole vielä pelastettu
    patient_list = []
    # print(f"\nPatient locations: ")
    while len(patient_list) < 3:
        patient_no = random.randint(1, 12)
        sql_patient_no = f"SELECT location FROM patient WHERE id = '{patient_no}' AND rescued = 0"
        cursor = yhteys.cursor()
        cursor.execute(sql_patient_no)
        res_patient_no = cursor.fetchone()
        # peli arpoo aina 3 eri potilasta, mikäli pelastettavia potilaita on tarpeeksi jäljellä
        if res_patient_no is not None:
            if res_patient_no[0] not in patient_list:
                patient_list.append(res_patient_no[0])

    return patient_list

def player_location():
    sql_rescue_player = f"SELECT location FROM player"
    cursor = yhteys.cursor()
    cursor.execute(sql_rescue_player)
    res_rescue_player = cursor.fetchone()
    return res_rescue_player

def rescue_patient(patient_list):
    # tarkistetaan onko pelaajan sijainnissa potilasta, jota ei ole vielä pelastettu (rescued=0)
    res_rescue_player = player_location()
    if res_rescue_player is not None:
        player_loc = res_rescue_player[0]  # Extract the location from the tuple
        if player_loc in patient_list:
            sql_rescue_patient = f"SELECT id FROM patient WHERE rescued = 0 AND location = '{player_loc}'"
            cursor = yhteys.cursor()
            cursor.execute(sql_rescue_patient)
            res_rescue_patient = cursor.fetchall()

            if cursor.rowcount != 0:
                print(f"You have picked up one of your patients. Continue your mission!")
                update_rescue_patient = f"UPDATE patient SET rescued = 1 WHERE id = '{res_rescue_patient[0][0]}'"
                update_patient_qty = f"UPDATE player SET patient_qty = (patient_qty + 1) where id = 1"
                cursor.execute(update_patient_qty)
                cursor.execute(update_rescue_patient)
        else:
            if player_location()[0] != 'ENTR':
                print(f"There is no patient to be saved here. Continue your mission!")
    return


# tarkistetaan onko pelaaja saavuttanut tavoitteen
def victory():
    sql_victory = "SELECT patient_goal FROM player WHERE id = 1"
    cursor = yhteys.cursor()
    cursor.execute(sql_victory)
    res_victory = cursor.fetchone()
    res_victory = res_victory[0]
    return res_victory

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

    while not game_over:
        patient_goal = victory()
        if patient_goal != 12:
            distance_lista = distances()
            if len(distance_lista) == 0:
                game_over = True
            else:
                print(f"\nPatient locations: ")
                print(*patient_locations)
                rescue_patient(patient_locations)
                update_goal()
                if helicopter() < 1:
                    print(f"You haven't any patients in helicopter and you have space for 3 patients")
                if 1 <= helicopter() < 3:
                    print(f"Picked patients {helicopter()} - still space for {3 - helicopter()} more patients")
                if helicopter() == 3:
                    print(f"Picked patients {helicopter()} - helicopter is full "
                        f"and you have to return to the home hospital")
                print(f"Saved patients {victory()}")
                home_hospital()  # pelaajan ja kotisairaalan etäisyys:
                if victory() == 3 or victory() == 6 or victory() == 9:
                    print(player_location())
                    if player_location()[0] == 'ENTR':
                        patient_locations = patient_randomizer()  # arpoo 3 potilasta
                    print("Patient saved")
                    # jatka = input('Paina Enter -näppäintä jatkaaksesi: ')
                    # if jatka == '':
                    distances()
                    print(f"\nPatient locations: ")
                    print(*patient_locations)
                    destination()
                else:
                    destination()  # mahdolliset kohteet, mihin pelaaja tahtoo mennä

        if patient_goal == 12:
            print("voitit")
            win = True
    if game_over == True:
        print(f"Game over. You are out of range. :(")




        # def funktio(destination)
        # sijainti päivittyy
        # update komennolla päivitetään patient rescued (player.location == patient.location -> rescued = 1)
        # Annetaan uudet kohteet + kotisairaala destination -> def vaihtoehdot +
        # if player.location not in kotisairaala1 or kotisairaala2 ==> def vaihtoehdot antaa myös kotisairaalan tiedot
        # if location == kotisairaala --> get fuel x määrä
        # kun player uudes kohtees mis on potilas -> if patients_qty < 3 update rescued +1 ja patients_qty +1
        # if player.location == kotisairaala -> patient_goal = patient_goal + patients_qty,
        # jonka jälkeen patients_qty muutetaan nollaksi'

        # if patient_goal == 12 -> peli päättyy (voitto)
        # if def vaihtoehdot - rowcount == 0 -> peli päättyy (häviö) else print lentokentät
