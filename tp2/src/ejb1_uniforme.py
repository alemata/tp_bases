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

for x in range(0, 100):
    values = []
    for x in range(0, 10):
      values.append(np.random.random_integers(100))

    c.execute("INSERT INTO uniforme VALUES ({values})".format(values=",".join(map(str, values))))

conn.commit()

# ------------------- PRUEBAS ----------------------
db_name = 'db.datos_ejb1'
table = 'uniforme'
columns = []
histograms_diff = []
for n in range(1, 11):
  column = 'd' + str(n)
  cEstimator = ClassicHistogram(db_name, table, column, parameter=4)
  rEstimator = RealHistogram(db_name, table, column, parameter=4)
  sEstimator = DistributionSteps(db_name, table, column, parameter=4)

  points = []
  errors = []
  errors_2 = []
  for x in range(rEstimator.min_value, rEstimator.max_value + 1):
    ce = cEstimator.estimate_equal(x)
    se = sEstimator.estimate_equal(x)
    re = rEstimator.estimate_equal(x)
    points.append(x)
    errors.append(abs(ce - re))
    errors_2.append(abs(se - re))

  avg_classic_diff = sum(errors) / len(errors)
  avg_step_diff = sum(errors_2) / len(errors_2)

  columns.append(n)
  #Guardo la diferencia entre las medias de las diferencias absolutas.
  histograms_diff.append(abs(avg_classic_diff - avg_step_diff))


import matplotlib.pyplot as plt


plt.plot(columns, histograms_diff, 'ro')
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.2)
plt.yticks([0,0.1,0.2,0.3])
# Tweak spacing to prevent clipping of tick-labels
plt.subplots_adjust(bottom=0.15)
plt.show()
