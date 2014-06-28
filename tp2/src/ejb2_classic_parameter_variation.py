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
error_avgs_col = []
error_avgs = []
for par in range(1, 11):
  for n in range(1, 11):
    # Uniforme
    column = 'd' + str(n)
    cEstimator = ClassicHistogram(db_name, table, column, parameter=par)
    rEstimator = RealHistogram(db_name, table, column, parameter=par)
    error_avgs_col = []

    errors = []
    for x in range(rEstimator.min_value, rEstimator.max_value + 1):
      ce = cEstimator.estimate_equal(x)
      re = rEstimator.estimate_equal(x)
      errors.append(abs(ce - re))

    avg_classic_diff = sum(errors) / len(errors)
    error_avgs_col.append(avg_classic_diff)

  columns.append(par)
  error_avgs.append(sum(error_avgs_col) / float(len(error_avgs_col)))


import matplotlib.pyplot as plt


a = plt.plot(columns, error_avgs, 'ro')


# ------------------- NORMAL ----------------------
table = 'normal'
columns = []
error_avgs_col = []
error_avgs = []
for par in range(1, 11):
  for n in range(1, 11):
    column = 'd' + str(n)
    cEstimator = ClassicHistogram(db_name, table, column, parameter=par)
    rEstimator = RealHistogram(db_name, table, column, parameter=par)
    error_avgs_col = []

    errors = []
    for x in range(rEstimator.min_value, rEstimator.max_value + 1):
      ce = cEstimator.estimate_equal(x)
      re = rEstimator.estimate_equal(x)
      errors.append(abs(ce - re))

    avg_classic_diff = sum(errors) / len(errors)
    error_avgs_col.append(avg_classic_diff)

  columns.append(par)
  error_avgs.append(sum(error_avgs_col) / float(len(error_avgs_col)))


import matplotlib.pyplot as plt


b = plt.plot(columns, error_avgs, 'b^')
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.2)
# Tweak spacing to prevent clipping of tick-labels
plt.subplots_adjust(bottom=0.15)
plt.legend( (a[0], b[0]), ('Uniforme', 'Normal') )
plt.ylabel('Error promedio')
plt.xlabel('Cantidad de bins')
plt.show()


# Como era de esperar mejora a medida que agrandamos el parameter. Esto es porque separa mejor los caso y entonces se tiene
# una estimacion mas precisa. El idea que seria que en cada bucket este 1 solo valor => la estimacion seria perfecta... pero
# eso tiene un costo espacial y computacional grande (igual a no hacer el histograma y usar la tabla directamente)
