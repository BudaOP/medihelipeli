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

def patient_location():
    icaolista = []
    while len(icaolista) < 12:
        m = random.randint(2, 21)
        if m not in icaolista:
            icaolista.append(m)

    b = 0
    c = 1
    for i in range(12):
        uus = icaolista[b]
        print(uus)
        sql = (f"UPDATE patient SET location = (SELECT ident FROM airport WHERE airport.id = '{uus}' "
               f"AND patient.id in(select patient.id from patient where patient.id = '{c}'))");
        print(sql)
        b = b + 1
        c = c + 1
        kursori = yhteys.cursor()
        kursori.execute(sql)
        # tulos = kursori.fetchall()
    return

# print()
patient_location()