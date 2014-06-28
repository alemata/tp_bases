# -*- coding: utf-8 -*-
from distribution_steps import DistributionSteps
from classic_histogram import ClassicHistogram
from real_histogram import RealHistogram
import math

import sqlite3
import numpy as np
import matplotlib.pyplot as plt

db_name = 'db.sqlite3'

table = 'table1'
max_errors = []
cols = []
param = 10
max_error_bound = 1 / float(param)
for col in range(0, 10):
  params = []
  column = 'c' + str(col)
  cols.append(col)
  rEstimator = RealHistogram(db_name, table, column, parameter=1)

  sEstimator = DistributionSteps(db_name, table, column, parameter=param)

  errors = []
  for x in range(rEstimator.min_value, rEstimator.max_value + 1):
    se = sEstimator.estimate_equal(x)
    re = rEstimator.estimate_equal(x)
    errors.append(abs(se - 0))

  max_errors.append(max(errors))

column_max_error = plt.plot(cols, max_errors, 'ro')

error_plot_x = []
error_plot = []
for x in range(-2, 11):
  error_plot_x.append(x)
  error_plot.append(max_error_bound)

error_bound = plt.plot(error_plot_x, error_plot)

plt.ylabel('Error maximo')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10])
plt.xlabel('Numero de columna')
plt.legend( (column_max_error[0], error_bound[0]), ('Maximo error', 'Cota error') )
plt.show()
