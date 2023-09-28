# funktiot
import random
import mysql.connector
from geopy import distance

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='Astr0n4utt1?',
         autocommit=True
         )

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

def measure_distance():

    # pelaajan sijainnin koordinaatit

    sql_player_coord = f"SELECT latitude_deg, longitude_deg from airport"
    sql_player_coord += f" where ident in (select location from player)"

    cursor = yhteys.cursor()
    cursor.execute(sql_player_coord)
    res_player_coord = cursor.fetchall()

    # ohjelma hakee kaikkien lentokenttien koordinaatit (pl. pelaajan sijainti)

    sql_airport_coord = f"SELECT latitude_deg, longitude_deg from airport"
    sql_airport_coord += f" where ident not in (select location from player)"

    cursor.execute(sql_airport_coord)
    res_airport_coord = cursor.fetchall()

    # ohjelma hakee kaikkien lentokenttien kunnat ja icao-koodit

    sql_municipality = f"SELECT municipality, ident from airport"
    sql_municipality += f" where ident not in (select location from player)"

    cursor.execute(sql_municipality)
    res_municipality = cursor.fetchall()

    # vertailu kotisairaalaan

    sql_home_coord = f"SELECT latitude_deg, longitude_deg from airport"
    sql_home_coord += f" where ident = 'ENTR'"

    cursor.execute(sql_player_coord)
    res_home_coord = cursor.fetchall()

    # ohjelma kertoo jos pelaaja on kotisairaalassa tai mikä olisi etäisyys sinne

    comparison_home = distance.distance({res_player_coord[0]}, {res_home_coord[0]})
    if comparison_home == 0:
        print(f"You are at the home hospital")

    else:
        print(f"Etäisyys kotisairaalaan on {comparison_home}")

    # hakee pelaajan sen hetkisen rangen

    sql_range = f"SELECT range_km from player"
    cursor.execute(sql_range)
    res_range = cursor.fetchone()

    print(f"Your current range is {res_range[0]} kilometers")
    print(f"\nThese locations are within your range:")

    # vertailu muihin kuntiin kuin kotisairaalaan
    # mikäli range riittää toiseen kuntaan, ohjelma tulostaa kunnan nimen ja heliportin icao-koodin

    for i in range(20):
        # print(f"{distance.distance({res_player_coord[0]}, {res_airport_coord[i]}).km:.2f} km")
        comparison = distance.distance({res_player_coord[0]}, {res_airport_coord[i]})

        if comparison <= float(res_range[0]):
            print(f"{res_municipality[i]} - {comparison}")


    return
def destination(): #kohde minne haluat matkustaa
    destination = input('Type the ICAO code: ')


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

measure_distance()

# hakee tietokannasta tiedot sijainnista ja potilaista (polttoainetiedot jne)
# kysyy minne haluat lentää seuraavaksi ja [näyttää lento vaihtoehdot ja ranget] -> def measure_distance()

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
