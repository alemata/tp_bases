import sqlite3
import numpy as np
import math

# Genero los datos con distribucion normal y uniforme

db_name = 'db.datos_normal_uniforme'
conn = sqlite3.connect(db_name)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS uniforme (d1 integer,d2 integer,d3 integer,d4 integer,d5 integer,d6 integer,d7 integer,d8 integer,d9 integer,d10 integer)")
c.execute("CREATE TABLE IF NOT EXISTS normal   (d1 integer,d2 integer,d3 integer,d4 integer,d5 integer,d6 integer,d7 integer,d8 integer,d9 integer,d10 integer)")
c.execute("DELETE from  uniforme")
c.execute("DELETE from  normal")

for x in range(0, 1000):
  values_uniforme = []
  values_normal = []

  for j in range(0, 10):
    values_uniforme.append(np.random.random_integers(100))
    values_normal.append(math.floor(np.random.normal(100, 10, 1)[0]))

  c.execute("INSERT INTO uniforme VALUES ({values})".format(values=",".join(map(str, values_uniforme))))
  c.execute("INSERT INTO normal VALUES ({values})".format(values=",".join(map(str, values_normal))))


conn.commit()
