# -*- coding: utf-8 -*-
from distribution_steps import DistributionSteps
from classic_histogram import ClassicHistogram
from real_histogram import RealHistogram
from estimator_group import EstimatorGroup
import math

import sqlite3
import numpy as np


db_name = 'db.datos_normal_uniforme'
table = 'normal'
columns = []
max_errors_classic = []
max_errors_steps = []
max_errors_group = []
param = 4
for n in range(1, 11):
  column = 'd' + str(n)
  cEstimator = ClassicHistogram(db_name, table, column, param)
  rEstimator = RealHistogram(db_name, table, column, param)
  sEstimator = DistributionSteps(db_name, table, column, param)
  gEstimator = EstimatorGroup(db_name, table, column, {'size': param, 'threshold': 0.018})

  points = []
  classic_errors = []
  step_errors = []
  group_errors = []
  for x in range(rEstimator.min_value, rEstimator.max_value + 1):
    ce = cEstimator.estimate_equal(x)
    se = sEstimator.estimate_equal(x)
    re = rEstimator.estimate_equal(x)
    ge = gEstimator.estimate_equal(x)
    points.append(x)
    classic_errors.append(abs(ce - re))
    step_errors.append(abs(se - re))
    group_errors.append(abs(ge - re))

  max_errors_classic.append(max(classic_errors))
  max_errors_steps.append(max(step_errors))
  max_errors_group.append(max(group_errors))

  columns.append(n)


import matplotlib.pyplot as plt


a = plt.plot(columns, max_errors_classic, 'ro')
b = plt.plot(columns, max_errors_steps, 'bo')
c = plt.plot(columns, max_errors_group, 'g^')
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.2)
# Tweak spacing to prevent clipping of tick-labels
plt.subplots_adjust(bottom=0.15)
plt.xticks(columns)
plt.legend( (a[0], b[0], c[0]), ('Classic', 'Steps', 'Group') )
plt.ylabel('Maximo error')
plt.xlabel('Numero de columna')
plt.show()
