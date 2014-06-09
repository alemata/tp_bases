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
    table_name = "classic_{0}".format(self.column)
    c.execute("CREATE TABLE IF NOT EXISTS {0} (border integer, amount integer, cumulative integer)".format(table_name))
    c.execute("DELETE FROM {0}".format(table_name))

    self.min_value, self.max_value, self.total_elem = c.execute(
        "SELECT min({0}), max({0}), count(*) FROM {1}".format(self.column, self.table)).fetchone()
    bucket = math.floor((self.max_value - self.min_value) / self.parameter)
    print "min: " + str(self.min_value)
    print "max: " + str(self.max_value)
    print "total_elem: " + str(self.total_elem)
    print "bucket size: " + str(bucket)
    prev_value = self.min_value
    next_value = prev_value
    total = 0
    self.borders = {}
    self.bucket_size = bucket

    while total != self.total_elem:
      if next_value == self.min_value:
        a = "SELECT count(*) FROM {0} where {1} = {2}".format(self.table, self.column, self.min_value)
      else:
        a = "SELECT count(*) FROM {0} where {1} > {2} AND {1} <= {3}".format(self.table, self.column,
                                                                             prev_value, next_value)
      amount = c.execute(a).fetchone()[0]
      print a + " => " + str(amount)
      total += amount
      self.borders[next_value] = {'amount': amount, 'cumulative': total}
      prev_value = next_value
      next_value += bucket

    conn.commit()
    conn.close()
    print "----------Finalizada la creacion de la estructura----------------"

  def estimate_equal(self, value):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    table_name = "classic_{0}".format(self.column)

    # Si es un borde entonces busco el valor directamente
    borders = c.execute("select border from {0}".format(table_name)).fetchall()
    if value < self.min_value or value > self.max_value:
      estimator = 0
    elif value in self.borders:
      amount = self.borders[value]['amount']
      estimator = (amount / float(self.total_elem))
      print "El estimador de {0} es: {1}".format(value, estimator)
    else:
      for i, val in enumerate(sorted(self.borders)):
        # Encontrar el bean donde se encuentra value
        if value < val:
          border = val
          break
      amount = self.borders[border]['amount']
      estimator = (amount / float(self.total_elem))
      print "El estimador de {0} es: {1}".format(value, estimator)

    return estimator

  def estimate_greater(self, value):
    return 1 - self.estimate_lower(value)

  def estimate_lower(self, value):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    table_name = "classic_{0}".format(self.column)

    # Si es un borde entonces busco el valor directamente
    if value < self.min_value:
      estimator = 0
    elif value > self.max_value:
      estimator = 1
    elif value in self.borders:
      amount = self.borders[value]['cumulative']
      estimator = (amount / float(self.total_elem))
      print "El estimador de {0} es: {1}".format(value, estimator)
    else:
      for i, val in enumerate(sorted(self.borders)):
        # Encontrar el bean donde se encuentra value
        if value < val:
          border = val
          break
      amount = self.borders[border]['cumulative']
      estimator = (amount / float(self.total_elem))
      print "El estimador de {0} es: {1}".format(value, estimator)

    return estimator
