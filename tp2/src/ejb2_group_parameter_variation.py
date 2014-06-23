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

# Genero los datos con distribucion uniforme
db_name = 'db.normal_uniforme'
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
error_avgs = []
for n in frange(0.001, 0.1, 0.003):
  column = 'd1'
  cEstimator = EstimatorGroup(db_name, table, column, {'size': 4, 'variance': n})
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
  cEstimator = EstimatorGroup(db_name, table, column, {'size': 4, 'variance': n})
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
# plt.legend( (a[0], b[0]), ('Uniforme', 'Normal') )
plt.ylabel('Maximo error')
plt.xlabel('Limite de variacion')
plt.show()

# En este caso solo variamos el parametro de la varianza 
# (ya que al ser una mejora de classic distribution, la variacion d parametro steps se comporta 
# de igual manera que el classic distribution, haria falta grafico?? No creo)
# 
