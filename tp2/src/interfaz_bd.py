# -*- coding: utf-8 -*-

# interfaz_bd.py : Implementar las consultas.
import sqlite3
import numpy as np

conn = sqlite3.connect('db.prueba')

c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS personas (dni text, nombre text, apellido text, edad integer)")
c.execute("DELETE from  personas")

c.execute("INSERT INTO personas VALUES ('33252352','Alejandro','Mataloni', 26)")
c.execute("INSERT INTO personas VALUES ('35542678','Marisol','Reartes', 23)")
c.execute("INSERT INTO personas VALUES ('3452352','Maria Lara','Gauder', 24)")
c.execute("INSERT INTO personas VALUES ('32990876','Emiliano','Mancuso', 27)")


conn.commit()
