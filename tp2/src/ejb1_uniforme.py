# -*- coding: utf-8 -*-
from distribution_steps import DistributionSteps
from classic_histogram import ClassicHistogram
from real_histogram import RealHistogram

import sqlite3
import numpy as np

# Genero los datos con distribucion uniforme
conn = sqlite3.connect('db.datos_ejb1')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS uniforme (d1 integer,d2 integer,d3 integer,d4 integer,d5 integer,d6 integer,d7 integer,d8 integer,d9 integer,d10 integer)")
c.execute("DELETE from  uniforme")

for x in range(0, 3000):
    values = []
    for x in range(0, 10):
      values.append(np.random.random_integers(100))

    c.execute("INSERT INTO uniforme VALUES ({values})".format(values=",".join(map(str, values))))

conn.commit()

# ------------------- PRUEBAS ----------------------
db_name = 'db.datos_ejb1'
table = 'uniforme'
columns = []
max_errors_classic = []
max_errors_steps = []
param = 4
for n in range(1, 11):
  column = 'd' + str(n)
  cEstimator = ClassicHistogram(db_name, table, column, param)
  rEstimator = RealHistogram(db_name, table, column, param)
  sEstimator = DistributionSteps(db_name, table, column, param)

  points = []
  classic_errors = []
  step_errors = []
  for x in range(rEstimator.min_value, rEstimator.max_value + 1):
    ce = cEstimator.estimate_equal(x)
    se = sEstimator.estimate_equal(x)
    re = rEstimator.estimate_equal(x)
    points.append(x)
    classic_errors.append(abs(ce - re))
    step_errors.append(abs(se - re))

  max_errors_classic.append(max(classic_errors))
  max_errors_steps.append(max(step_errors))

  columns.append(n)


import matplotlib.pyplot as plt


a = plt.plot(columns, max_errors_classic, 'ro')
b = plt.plot(columns, max_errors_steps, 'bo')
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.2)
# Tweak spacing to prevent clipping of tick-labels
plt.yticks([0,0.1,0.2,0.3, 0.4])
plt.subplots_adjust(bottom=0.15)
plt.legend( (a[0], b[0]), ('Classic', 'Steps') )
plt.show()
