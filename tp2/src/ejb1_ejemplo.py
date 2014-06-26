# -*- coding: utf-8 -*-

# interfaz_bd.py : Implementar las consultas.
import sqlite3
import numpy as np

conn = sqlite3.connect('db.ejemplo')

c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS ejemplo (d1 integer)")
c.execute("DELETE from  ejemplo")

c.execute("INSERT INTO ejemplo VALUES (0)")
c.execute("INSERT INTO ejemplo VALUES (1)")
c.execute("INSERT INTO ejemplo VALUES (3)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (4)")
c.execute("INSERT INTO ejemplo VALUES (5)")
c.execute("INSERT INTO ejemplo VALUES (7)")
c.execute("INSERT INTO ejemplo VALUES (7)")
c.execute("INSERT INTO ejemplo VALUES (9)")
c.execute("INSERT INTO ejemplo VALUES (12)")


conn.commit()


from distribution_steps import DistributionSteps
from classic_histogram import ClassicHistogram
from estimator_group import EstimatorGroup
from real_histogram import RealHistogram

# Creo una instancia de la clase que representa al metodo
# 'Histograma Clasico'
classicEstimator = ClassicHistogram('db.ejemplo', 'ejemplo', 'd1', 4)
stepEstimator = DistributionSteps('db.ejemplo', 'ejemplo', 'd1', 4)
# Pruebo distintas instancias de estimacion
# print "Classic Histogram"
print "Sel(=%d) : %3.2f" % (5, classicEstimator.estimate_equal(5))
print "Sel(=%d) : %3.2f" % (5, stepEstimator.estimate_equal(5))


import matplotlib.pyplot as plt

# Classic
x = [-3, 0, 3, 6, 9]

k=[1,2,13,3,1]

ax = plt.subplot(111)
plt.xticks([-3, 0, 3, 6, 9,12])
classic = ax.bar(x, k, width=3, color='r',align='edge')
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

bx = plt.subplot(111)
x = [-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12]
k = [0,0,0,1,1,0,1,12,1,0,2,0,1,0,0,1]
plt.xticks(x)
real = bx.bar(x, k, width=0.2, color='b', align='center')
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])


plt.ylabel('Cantidad de apariciones')
plt.xlabel('Valor')
plt.legend( (classic[0], real[0]), ('Histograma clasico', 'Real') )
plt.show()

# Step
bx = plt.subplot(111)
x = [0,1,2,3,4]

k=[5,5,5,5,0]
labels = ['0', '(1,4)', '(2,4)', '(3,4)', '(4,12)']
plt.xticks(x, labels)
steps = bx.bar(x, k, width=1, color='r',align='edge')
plt.axis([0, 6, 0, 8])
plt.yticks([0,1,2,3,4,5,6,7,8])
plt.legend( [steps[0]], ['Steps'] )
plt.ylabel('Altura')
plt.xlabel('(Borde, Valor)')

plt.show()

