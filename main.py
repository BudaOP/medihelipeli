# funktiot
def backlore():
    print('backlore - tavoite')

def destination(): #kohde minne haluat matkustaa
    destination = input('Kirjoita icao koodi minne haluat matkustaa')


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