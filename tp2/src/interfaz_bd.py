# -*- coding: utf-8 -*-

# interfaz_bd.py : Implementar las consultas.
import sqlite3
import numpy as np

conn = sqlite3.connect('db.prueba')

c = conn.cursor()

# Ej_b_1
# c.execute("CREATE TABLE IF NOT EXISTS personas (dni text, nombre text, apellido text, edad integer)")
# c.execute("DELETE from  personas")



# c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 0)")
# c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 2)")
# c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 3)")

# for x in range(0, 13):
    # c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 4)")

# c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 7)")
# c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 7)")
# c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 8)")
# c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 12)")


c.execute("CREATE TABLE IF NOT EXISTS personas (d1 integer,d2 integer,d3 integer,d4 integer,d5 integer,d6 integer,d7 integer,d8 integer,d9 integer,d10 integer)")
c.execute("DELETE from  personas")


for x in range(0, 100):
    values = []
    for x in range(0, 10):
      values.append(np.random.random_integers(100))

    c.execute("INSERT INTO personas VALUES ({values})".format(values=",".join(map(str, values))))


conn.commit()
