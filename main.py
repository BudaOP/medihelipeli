import random
import mysql.connector
from geopy import distance
from tabulate import tabulate

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='ronistrom',
         autocommit=True
         )


# FUNKTIOT


def start():
    screen_name = input("What's your name? ")
    sql_start = (f"UPDATE player SET screen_name = '{screen_name}', "
                 f"location = 'ENTR', patient_goal = 0, patient_qty = 0, "
                 f"range_km = 400 WHERE id = 1")

    cursor = yhteys.cursor()
    cursor.execute(sql_start)
    return

def lore():
    print(f'*backlore will be here*')
    return


def player_coord():
    # pelaajan sijainnin koordinaatit
    sql_player_coord = f"SELECT latitude_deg, longitude_deg from airport"
    sql_player_coord += f" where ident in (select location from player)"

    cursor = yhteys.cursor()
    cursor.execute(sql_player_coord)
    res_player_coord = cursor.fetchall()
    return res_player_coord

def distances():
    # ohjelma hakee kaikkien lentokenttien koordinaatit (pl. pelaajan sijainti)
    sql_airport_coord = f"SELECT latitude_deg, longitude_deg from airport"
    sql_airport_coord += f" where ident not in (select location from player)"

    cursor = yhteys.cursor()
    cursor.execute(sql_airport_coord)
    res_airport_coord = cursor.fetchall()

    # ohjelma hakee kaikkien lentokenttien kunnat ja icao-koodit
    sql_municipality = f"SELECT municipality from airport"
    sql_municipality += f" where ident not in (select location from player)"

    cursor.execute(sql_municipality)
    res_municipality = cursor.fetchall()

    # ohjelma hakee kaikkien lentokenttien kunnat ja icao-koodit
    sql_icao = f"SELECT ident from airport"
    sql_icao += f" where ident not in (select location from player)"

    cursor.execute(sql_icao)
    res_icao = cursor.fetchall()

    # ohjelma kertoo pelaajan jäljellä olevan rangen
    print(f"Your current range is {player_range()[0]} kilometers")
    print(f"\nThese locations are within your range:")

    # vertailu muihin kuntiin kuin kotisairaalaan
    # mikäli range riittää toiseen kuntaan, ohjelma tulostaa kunnan nimen ja heliportin icao-koodin

    lista = []
    for i in range(20):
        # print(f"{distance.distance({res_player_coord[0]}, {res_airport_coord[i]}).km:.2f} km")
        comparison = int(distance.distance({player_coord()[0]}, {res_airport_coord[i]}).km)

        if comparison <= float(player_range()[0]):
            lista.append([res_municipality[i][0], res_icao[i][0], comparison])

            # print(f"{res_municipality[i][0]} - {res_icao[i][0]} - {comparison}")
    print(tabulate(lista, headers=['Location', 'ICAO', 'Distance(km)']))
    return


def home_hospital():
    # vertailu kotisairaalaan
    sql_home_coord = f"SELECT latitude_deg, longitude_deg from airport"
    sql_home_coord += f" where ident = 'ENTR'"

    cursor = yhteys.cursor()
    cursor.execute(sql_home_coord)
    res_home_coord = cursor.fetchall()

    # ohjelma kertoo jos pelaaja on kotisairaalassa tai mikä olisi etäisyys sinne
    comparison_home = distance.distance({player_coord()[0]}, {res_home_coord[0]})
    if comparison_home == 0:
        print(f"You are at the home hospital")

    else:
        print(f"Your distance to the home hospital is {comparison_home}")
    return


def player_range():
    # hakee pelaajan sen hetkisen rangen
    sql_range = f"SELECT range_km from player"
    
    cursor = yhteys.cursor()
    cursor.execute(sql_range)
    res_range = cursor.fetchone()
    return res_range


def destination(): #kohde minne haluat matkustaa
    new_location = input('Type the ICAO code: ')
    sql_icao_coord = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '{new_location}'"
    cursor = yhteys.cursor()
    cursor.execute(sql_icao_coord)
    res_icao_coord = cursor.fetchall()

    #Lasketaan, riittääkö range halutulle lentokentälle
    if cursor.rowcount > 0:
        destination_distance = int(distance.distance(player_coord(), res_icao_coord).km)
        if destination_distance <= int(player_range()[0]):
            sql_update_location = (f"UPDATE player SET location = '{new_location}'")
            cursor = yhteys.cursor()
            cursor.execute(sql_update_location)
            print(f"You are now at {new_location}")

            # Päivitetään uusi range
            old_range = int(player_range()[0])
            new_range = old_range - destination_distance
            sql_new_range = (f"UPDATE player SET range_km = '{new_range}'")
            print(f"Your new range is {new_range} kilometers ")
        if destination_distance > int(player_range()[0]):
            print(f"You don't have enough range to travel to this destination ")
            destination()
    if cursor.rowcount == 0:
        print(f"Please try again")
        destination()
    return

    #Päivitetään uusi range
    old_range = int(player_range()[0])
    new_range = old_range - destination_distance
    sql_new_range = (f"UPDATE player SET range_km = '{new_range}'")
    print(f"Your new range is {new_range} kilometers ")
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
               f"WHERE patient.id = '{i+1}'")
        kursori = yhteys.cursor()
        kursori.execute(sql)

    return


# Pelin aloitus
aloitus = input('Do you want to start a new game? y/n: ')

# backlore

backlore = input('Would you like to read the backlore? y/n: ')
if backlore == "y":
    lore()

# säännöt pelaajalle
print('Game goal: save the patients')

start()

distances()

# hakee tietokannasta tiedot sijainnista ja potilaista (polttoainetiedot jne)
# kysyy minne haluat lentää seuraavaksi ja [näyttää lento vaihtoehdot ja ranget] -> def measure_distance()

home_hospital()
player_range()
destination()


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
