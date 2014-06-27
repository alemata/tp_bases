# -*- coding: utf-8 -*-
from distribution_steps import DistributionSteps
from classic_histogram import ClassicHistogram
from real_histogram import RealHistogram
import math

import sqlite3
import numpy as np
import matplotlib.pyplot as plt

db_name = 'db.sqlite3'
colors = ['ro', 'b^', 'gv', 'b<', 'b*', 'rs', 'g+', 'mp', 'y>', 'ko']

# ------------------- UNIFORME ----------------------
table = 'table1'
params = []
error_avgs_col = []
error_avgs = []
for col in range(0, 10):
  error_avgs_col = []
  params = []
  column = 'c' + str(col)
  rEstimator = RealHistogram(db_name, table, column, parameter=1)
  for par in range(2, 11, 2):
    print "arranque creacion---------"
    sEstimator = DistributionSteps(db_name, table, column, parameter=par)
    print "termine creacion---------"
    print par

    errors = []
    for x in range(rEstimator.min_value, rEstimator.max_value + 1):
      se = sEstimator.estimate_equal(x)
      re = rEstimator.estimate_equal(x)
      errors.append(abs(se - re))

    params.append(par)
    avg_classic_diff = sum(errors) / len(errors)
    error_avgs_col.append(avg_classic_diff)

  a = plt.plot(params, error_avgs_col, colors[col])

plt.margins(0.2)
plt.subplots_adjust(bottom=0.15)
plt.ylabel('Error promedio')
plt.xlabel('Cantidad de steps')
plt.show()
