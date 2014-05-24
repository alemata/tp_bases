# -*- coding: utf-8 -*-
import sqlite3
import numpy as np
import pylab
import random
import math

class Estimator(object):
  """Clase base de los estimadores."""

  def __init__(self, db, table, column, parameter=10):
    self.db = db
    self.table = table
    self.column = column
    self.parameter = parameter

    # Construye las estructuras necesita el estimador.
    self.build_struct()

  def build_struct(self):
    raise NotImplementedError()

  def estimate_equal(self, value):
    raise NotImplementedError()

  def estimate_greater(self, value):
    raise NotImplementedError()


class ClassicHistogram(Estimator):
  """Histograma clasico."""

  def build_struct(self):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    table_name = "classic_{0}".format(self.column)
    c.execute("CREATE TABLE IF NOT EXISTS {0} (border integer, amount integer, cumulative integer)".format(table_name))
    c.execute("DELETE FROM {0}".format(table_name))

    min_value, max_value, total_elem = c.execute("SELECT min({0}), max({0}), count(*) FROM {1}".format(self.column, self.table)).fetchone()
    bucket = math.floor((max_value - min_value) / self.parameter)
    print "min: " + str(min_value)
    print "max: " + str(max_value)
    print "bucket size: " + str(bucket)
    prev_value = min_value
    next_value = prev_value
    total = 0

    while total != total_elem:
      if next_value == min_value:
        a = "SELECT count(*) FROM {0} where {1} = {2}".format(self.table, self.column, min_value)
      else:
        a = "SELECT count(*) FROM {0} where {1} > {2} AND {1} <= {3}".format(self.table, self.column, prev_value, next_value )
      amount = c.execute(a).fetchone()[0]
      print a + " => " + str(amount)
      total += amount
      c.execute("INSERT INTO {0} VALUES ({1}, {2}, {3})".format(table_name, next_value, amount, total))
      prev_value = next_value
      next_value += bucket

    print total

    conn.commit()
    conn.close()
    print "----------Finalizada la creacion de la estructura----------------"


  def estimate_equal(self, value):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    table_name = "classic_{0}".format(self.column)

    # Calcular total de elementos de la tabla
    total_elem = "select cumulative from {0} order by cumulative DESC limit 1".format(table_name)
    total = c.execute(total_elem).fetchone()[0]

    # Si es un borde entonces busco el valor directamente
    borders = c.execute("select border from {0}".format(table_name)).fetchall()
    if (value,) in borders:
      a = "SELECT amount FROM {0} where border = {1}".format(table_name, value)
      amount = c.execute(a).fetchone()[0]
      estimator = (amount / float(total))
      print "El estimador de {0} es: {1}".format(value, estimator)
    else:
      for i, val in enumerate(borders):
        # Encontrar el bean donde se encuentra value
        if value < val[0]:
          border = val[0]
          break
      a = "SELECT amount FROM {0} where border = {1}".format(table_name, border)
      amount = c.execute(a).fetchone()[0]
      estimator = (amount / float(total))
      print "El estimador de {0} es: {1}".format(value, estimator)

    return estimator


  def estimate_greater(self, value):
    raise NotImplementedError()

