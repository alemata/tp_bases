# -*- coding: utf-8 -*-
from distribution_steps import DistributionSteps
from classic_histogram import ClassicHistogram
from real_histogram import RealHistogram

import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# ------------------- PRUEBAS ----------------------
db_name = 'db.sqlite3'
table = 'table1'
columns = []
histograms_diff = []
p_values = []
param = 100
for n in range(0, 10):
  column = 'c' + str(n)
  cEstimator = ClassicHistogram(db_name, table, column, parameter=param)
  rEstimator = RealHistogram(db_name, table, column, parameter=param)
  sEstimator = DistributionSteps(db_name, table, column, parameter=param)

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

  columns.append(n)
  paired_sample = stats.ttest_rel(errors, errors_2)
  p_values.append(paired_sample[1])
  print "The t-statistic is %.3f and the p-value is %.10f." % paired_sample


a = plt.plot(columns, p_values, 'ro')
plt.margins(0.2)
plt.ylabel('P-value')
plt.xlabel('Numero de columna')
plt.legend( [a[0]], ["P-value"] )
plt.subplots_adjust(bottom=0.15)
plt.show()
