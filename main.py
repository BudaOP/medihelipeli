# funktiot
import random
import mysql.connector

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='KierukkaKupariNöö7!',
         autocommit=True
         )



def backlore():
    print('backlore - tavoite')

def destination(): #kohde minne haluat matkustaa
    destination = input('Kirjoita icao koodi minne haluat matkustaa')

# patient location arpominen
def patient_location():
    icaolista = []
    while len(icaolista) < 12:
        m = random.randint(2,21)
        if m not in icaolista:
            icaolista.append(m)

    b = 0
    for i in range(12):
        sql = f"UPDATE patient SET location = (select ident from airport WHERE id = '{icaolista[b]}')"
        b += 1
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
    return tulos



# Pelin aloitus
aloitus = input('Haluatko aloittaa pelin? y/n: ')
backlore = input('Haluatko lukea backloren? y/n: ')
# backlore

if backlore == "y":
    backlore()

# säännöt pelaajalle
print('Pelasta potilaat mahdollisimman vähemmäl polttoaineel')

# hakee tietokannasta tiedot sijainnista ja potilaista (polttoainetiedot jne)
# kysyy minne haluat lentää seuraavaksi ja [näyttää lento vaihtoehdot ja ranget] -> def vaihtoehdot
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