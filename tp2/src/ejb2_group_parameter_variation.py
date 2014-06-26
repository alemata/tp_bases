# -*- coding: utf-8 -*-
from distribution_steps import DistributionSteps
from classic_histogram import ClassicHistogram
from real_histogram import RealHistogram
from estimator_group import EstimatorGroup
import math

import sqlite3
import numpy as np

def frange(start, stop, step):
  i = start
  while i < stop:
    yield i
    i += step

db_name = 'db.datos_normal_uniforme'

# ---------------- UNIFORME -----------------------
table = 'uniforme'
columns = []
error_avgs = []
for n in frange(0.001, 0.1, 0.003):
  column = 'd1'
  cEstimator = EstimatorGroup(db_name, table, column, {'size': 4, 'threshold': n})
  rEstimator = RealHistogram(db_name, table, column, parameter=n)

  errors = []
  for x in range(rEstimator.min_value, rEstimator.max_value + 1):
    ce = cEstimator.estimate_equal(x)
    re = rEstimator.estimate_equal(x)
    errors.append(abs(ce - re))

  avg_classic_diff = sum(errors) / len(errors)

  columns.append(n)
  error_avgs.append(avg_classic_diff)


import matplotlib.pyplot as plt


a = plt.plot(columns, error_avgs, 'ro')


# ------------------- NORMAL ----------------------
table = 'normal'
columns = []
error_avgs = []
for n in frange(0.001, 0.1, 0.003):
  column = 'd1'
  cEstimator = EstimatorGroup(db_name, table, column, {'size': 4, 'threshold': n})
  rEstimator = RealHistogram(db_name, table, column, parameter=n)

  errors = []
  for x in range(rEstimator.min_value, rEstimator.max_value + 1):
    ce = cEstimator.estimate_equal(x)
    re = rEstimator.estimate_equal(x)
    errors.append(abs(ce - re))

  # avg_classic_diff = sum(errors) / len(errors)
  avg_classic_diff = max(errors)

  columns.append(n)
  error_avgs.append(avg_classic_diff)


import matplotlib.pyplot as plt


b = plt.plot(columns, error_avgs, 'bo')
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.2)
# Tweak spacing to prevent clipping of tick-labels
plt.subplots_adjust(bottom=0.15)
plt.legend( (a[0], b[0]), ('Uniforme', 'Normal') )
plt.yticks([0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
# plt.legend( (a[0], b[0]), ('Uniforme', 'Normal') )
plt.ylabel('Maximo error')
plt.xlabel('Limite de variacion')
plt.show()

# En este caso solo variamos el parametro de la varianza
# (ya que al ser una mejora de classic distribution, la variacion d parametro steps se comporta
# de igual manera que el classic distribution, haria falta grafico?? No creo)
# Aclarar que aca usamos el maximo error porque el promedio no daba mucha informacion
# (suponemos que no resaltaba tanto el error que habia) en algunos valores (se lo comia el promedio)
