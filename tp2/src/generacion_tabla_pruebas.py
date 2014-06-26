import sqlite3
import numpy as np

# Genero los datos con distribucion normal y uniforme

db_name = 'db.datos_normal_uniforme'
conn = sqlite3.connect(db_name)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS uniforme (d1 integer)")
c.execute("DELETE from  uniforme")

c.execute("CREATE TABLE IF NOT EXISTS normal (d1 integer)")
c.execute("DELETE from  normal")


for x in range(0, 1000):
    uniform_value = np.random.random_integers(100)
    normal_value = math.floor(np.random.normal(100, 5, 1)[0])

    c.execute("INSERT INTO uniforme VALUES ({value})".format(value=uniform_value))
    c.execute("INSERT INTO normal VALUES ({value})".format(value=normal_value))

conn.commit()
