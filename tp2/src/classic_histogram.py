# -*- coding: utf-8 -*-
import estimators
import sqlite3
import numpy as np
import pylab
import random
import math

class ClassicHistogram(estimators.Estimator):
  """Histograma clasico."""

  def build_struct(self):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()

    self.min_value, self.max_value, self.total_elem = c.execute(
        "SELECT min({0}), max({0}), count(*) FROM {1}".format(self.column, self.table)).fetchone()

    bucket = math.floor((self.max_value - self.min_value) / self.parameter)
    prev_value = self.min_value
    next_value = prev_value
    total = 0
    self.borders = {}

    while total != self.total_elem:
      if next_value == self.min_value:
        a = "SELECT count(*) FROM {0} where {1} = {2}".format(self.table, self.column, self.min_value)
      else:
        a = "SELECT count(*) FROM {0} where {1} > {2} AND {1} <= {3}".format(self.table, self.column,
                                                                             prev_value, next_value)
      amount = c.execute(a).fetchone()[0]
      total += amount
      self.borders[next_value] = {'amount': amount, 'cumulative': total}
      prev_value = next_value
      next_value += bucket

    conn.commit()
    conn.close()

  def estimate_equal(self, value):
    if value < self.min_value or value > self.max_value:
      estimator = 0
    elif value in self.borders:
      # Si es un borde entonces busco el valor directamente
      amount = self.borders[value]['amount']
      estimator = (amount / float(self.total_elem))
    else:
      for i, val in enumerate(sorted(self.borders)):
        # Si no es un borde,
        # encontrar el bean donde se encuentra value
        if value < val:
          border = val
          break
      amount = self.borders[border]['amount']
      estimator = (amount / float(self.total_elem))

    return estimator

  def estimate_greater(self, value):
    return 1 - self.estimate_lower(value)

  def estimate_lower(self, value):
    if value < self.min_value:
      estimator = 0
    elif value > self.max_value:
      estimator = 1
    elif value in self.borders:
      # Si es un borde entonces busco el valor directamente
      amount = self.borders[value]['cumulative']
      estimator = (amount / float(self.total_elem))
    else:
      for i, val in enumerate(sorted(self.borders)):
        # Si no es un borde,
        # encontrar el bean donde se encuentra value
        if value < val:
          border = val
          break
      amount = self.borders[border]['cumulative']
      estimator = (amount / float(self.total_elem))

    return estimator
