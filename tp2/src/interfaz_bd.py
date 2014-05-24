# -*- coding: utf-8 -*-

# interfaz_bd.py : Implementar las consultas.
import sqlite3
conn = sqlite3.connect('db.prueba')

c = conn.cursor()

# Create table
c.execute("CREATE TABLE personas (dni text, nombre text, apellido text, edad integer)")


c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 10)")
c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 43)")
c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 49)")
c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 51)")
c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 60)")

for x in range(0, 5):
    c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 17)")
    c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 32)")
    c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 37)")
for x in range(0, 40):
    c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 22)")
    c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 28)")

conn.commit()
