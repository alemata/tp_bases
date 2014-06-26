# -*- coding: utf-8 -*-
from distribution_steps import DistributionSteps
from classic_histogram import ClassicHistogram
from real_histogram import RealHistogram
import math

import sqlite3
import numpy as np

db_name = 'db.datos_normal_uniforme'

# ------------------- UNIFORME ----------------------
table = 'uniforme'
columns = []
error_avgs = []
for n in range(1, 11):
  # Uniforme
  column = 'd1'
  sEstimator = DistributionSteps(db_name, table, column, parameter=n)
  rEstimator = RealHistogram(db_name, table, column, parameter=n)

  errors = []
  for x in range(rEstimator.min_value, rEstimator.max_value + 1):
    se = sEstimator.estimate_equal(x)
    re = rEstimator.estimate_equal(x)
    errors.append(abs(se - re))

  avg_classic_diff = sum(errors) / len(errors)

  columns.append(n)
  error_avgs.append(avg_classic_diff)


import matplotlib.pyplot as plt


a = plt.plot(columns, error_avgs, 'ro')


# ------------------- NORMAL ----------------------
table = 'normal'
columns = []
error_avgs = []
for n in range(1, 11):
  # Uniforme
  column = 'd1'
  sEstimator = ClassicHistogram(db_name, table, column, parameter=n)
  rEstimator = RealHistogram(db_name, table, column, parameter=n)

  errors = []
  for x in range(rEstimator.min_value, rEstimator.max_value + 1):
    se = sEstimator.estimate_equal(x)
    re = rEstimator.estimate_equal(x)
    errors.append(abs(se - re))

  avg_classic_diff = sum(errors) / len(errors)

  columns.append(n)
  error_avgs.append(avg_classic_diff)


import matplotlib.pyplot as plt

b = plt.plot(columns, error_avgs, 'bo')
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.2)
# Tweak spacing to prevent clipping of tick-labels
plt.subplots_adjust(bottom=0.15)
plt.legend( (a[0], b[0]), ('Uniforme', 'Normal') )
plt.ylabel('Error promedio')
plt.xlabel('Numero de steps')
plt.show()

# Aca por un error el en codigo al principio daban igual con todos los parameters.. (podriamos chamuyar algo en el informe
# con esto)
# Como era de esperar mejora a medida que agrandamos el parameter. Esto es porque separa mejor los caso y entonces se tiene 
# una estimacion mas precisa. El idea que seria que en cada bucket este 1 solo valor => la estimacion seria perfecta... pero
# eso tiene un costo espacial y computacional grande (igual a no hacer el histograma y usar la tabla directamente)

