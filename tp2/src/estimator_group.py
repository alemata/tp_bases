# -*- coding: utf-8 -*-
import estimators
import sqlite3
import numpy as np
import pylab
import random
import math

class EstimatorGroup(estimators.Estimator):
  """Estimador clasico con mejora en buckets de mucha varianza."""

  def build_struct(self):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()

    self.min_value, self.max_value, self.total_elem = c.execute(
        "SELECT min({0}), max({0}), count(*) FROM {1}".format(self.column, self.table)).fetchone()

    self.bucket = int(math.floor((self.max_value - self.min_value) / self.parameter['size']))
    prev_value = self.min_value
    next_value = int(prev_value)
    total = 0
    self.borders = {}
    self.real_values = {}

    while total != self.total_elem:
      if next_value == self.min_value:
        a = "SELECT count(*) FROM {0} where {1} = {2}".format(self.table, self.column, self.min_value)
        amount = c.execute(a).fetchone()[0]
        total += amount
        self.borders[next_value] = {'amount': amount, 'cumulative': total}
      else:
        # Calculo la varianza de los estimadores
        range_to_test = range(prev_value + 1, next_value + 1)
        real_values_count_tmp = {}
        real_estimators_dict_tmp = {}
        for x in range_to_test:
          a = "SELECT count(*) FROM {0} where {1} = {2}".format(self.table, self.column, x)
          a_value = c.execute(a).fetchone()[0]
          real_values_count_tmp[x] = a_value
          real_estimators_dict_tmp[x] = a_value / float(self.total_elem)

        # print real_estimators_dict_tmp
        # print np.var(real_estimators_dict_tmp.values())
        # print "------------------"
        threshold = np.var(real_estimators_dict_tmp.values())

        max_val = max(real_estimators_dict_tmp.values())
        min_val = min(real_estimators_dict_tmp.values())
        diff =  abs(max_val - min_val)
        if diff >= self.parameter['threshold']:
          # Si la maxima diferencia de la estimacion es mayor a
          # la pasada por parametro guardo los valores exactos
          self.real_values.update(real_values_count_tmp)

          total += sum(real_values_count_tmp.values())
          self.borders[next_value] = {'amount': -1, 'cumulative': -1}
        else:
          a = "SELECT count(*) FROM {0} where {1} > {2} AND {1} <= {3}".format(self.table, self.column,
                                                                               prev_value, next_value)
          amount = c.execute(a).fetchone()[0]
          total += amount
          self.borders[next_value] = {'amount': amount, 'cumulative': total}

      prev_value = next_value
      next_value += self.bucket

    conn.commit()
    conn.close()
    # print self.print_borders()
    # print self.real_values

  def estimate_equal(self, value):
    if value < self.min_value or value > self.max_value:
      estimator = 0
    elif value in self.borders:
      # Si es un borde entonces busco el valor directamente
      amount = self.borders[value]['amount']
    else:
      for i, val in enumerate(sorted(self.borders)):
        # Si no es un borde,
        # encontrar el bean donde se encuentra value
        if value < val:
          border = val
          break
      amount = self.borders[border]['amount']

    # Si es -1 es porque tengo el valor exacto guardado.
    if amount == -1:
      amount = self.real_values[value]

    estimator = amount / float(self.total_elem)

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
      # Si el valor es -1 voy hasta el primer bucket
      # anterior que tenga amount != -1
      if amount == -1:
        while amount == -1:
          prev_value = value - self.bucket
          amount = self.borders[prev_value]['cumulative']
      for x in range(prev_value + 1, value + 1):
        amount += self.real_values[x]
    else:
      for i, val in enumerate(sorted(self.borders)):
        # Si no es un borde,
        # encontrar el bean donde se encuentra value
        if value < val:
          border = val
          break
      amount = self.borders[border]['cumulative']
      if amount == -1:
        while amount == -1:
          prev_value = border - self.bucket
          amount = self.borders[prev_value]['cumulative']
      for x in range(prev_value + 1, value + 1):
        amount += self.real_values[x]


    estimator = (amount / float(self.total_elem))
    return estimator


  def print_borders(self):
    for i, val in enumerate(sorted(self.borders)):
      print "{val} : {value}".format(val=val, value=self.borders[val])
