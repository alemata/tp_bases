# -*- coding: utf-8 -*-
from distribution_steps import DistributionSteps
from classic_histogram import ClassicHistogram
from real_histogram import RealHistogram
import math

import sqlite3
import numpy as np

# Genero los datos con distribucion uniforme
db_name = 'db.variacion_classic'
# conn = sqlite3.connect(db_name)
# c = conn.cursor()

# c.execute("CREATE TABLE IF NOT EXISTS uniforme (d1 integer)")
# c.execute("DELETE from  uniforme")

# c.execute("CREATE TABLE IF NOT EXISTS normal (d1 integer)")
# c.execute("DELETE from  normal")


# for x in range(0, 1000):
    # uniform_value = np.random.random_integers(100)
    # normal_value = math.floor(np.random.normal(100, 5, 1)[0])

    # c.execute("INSERT INTO uniforme VALUES ({value})".format(value=uniform_value))
    # c.execute("INSERT INTO normal VALUES ({value})".format(value=normal_value))

# conn.commit()

# ------------------- UNIFORME ----------------------
table = 'uniforme'
columns = []
histograms_diff = []
for n in range(1, 11):
  # Uniforme
  column = 'd1'
  cEstimator = ClassicHistogram(db_name, table, column, parameter=n)
  rEstimator = RealHistogram(db_name, table, column, parameter=n)

  errors = []
  for x in range(rEstimator.min_value, rEstimator.max_value + 1):
    ce = cEstimator.estimate_equal(x)
    re = rEstimator.estimate_equal(x)
    errors.append(abs(ce - re))

  avg_classic_diff = sum(errors) / len(errors)

  columns.append(n)
  #Guardo la diferencia entre las medias de las diferencias absolutas.
  histograms_diff.append(avg_classic_diff)


import matplotlib.pyplot as plt


a = plt.plot(columns, histograms_diff, 'ro')


# ------------------- NORMAL ----------------------
db_name = 'db.variacion_classic'
table = 'normal'
columns = []
histograms_diff = []
for n in range(1, 11):
  # Uniforme
  column = 'd1'
  cEstimator = ClassicHistogram(db_name, table, column, parameter=n)
  rEstimator = RealHistogram(db_name, table, column, parameter=n)

  errors = []
  for x in range(rEstimator.min_value, rEstimator.max_value + 1):
    ce = cEstimator.estimate_equal(x)
    re = rEstimator.estimate_equal(x)
    errors.append(abs(ce - re))

  avg_classic_diff = sum(errors) / len(errors)

  columns.append(n)
  #Guardo la diferencia entre las medias de las diferencias absolutas.
  histograms_diff.append(avg_classic_diff)


import matplotlib.pyplot as plt


b = plt.plot(columns, histograms_diff, 'bo')
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.2)
# Tweak spacing to prevent clipping of tick-labels
plt.subplots_adjust(bottom=0.15)
plt.legend( (a[0], b[0]), ('Uniforme', 'Normal') )
plt.ylabel('Error promedio')
plt.xlabel('Numero de steps')
plt.show()


# Como era de esperar mejora a medida que agrandamos el parameter. Esto es porque separa mejor los caso y entonces se tiene 
# una estimacion mas precisa. El idea que seria que en cada bucket este 1 solo valor => la estimacion seria perfecta... pero
# eso tiene un costo espacial y computacional grande (igual a no hacer el histograma y usar la tabla directamente)
