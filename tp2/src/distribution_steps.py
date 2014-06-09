# -*- coding: utf-8 -*-
import estimators
import sqlite3
import numpy as np
import pylab
import random
import math

class DistributionSteps(estimators.Estimator):
  """Histograma usando steps."""

  def build_struct(self):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()

    self.min_value, self.max_value, self.total_elem = c.execute(
      "SELECT min({0}), max({0}), count(*) FROM {1}".format(self.column, self.table)).fetchone()

    self.step_height = math.floor(self.total_elem / self.parameter)
    self.steps = []

    offset = self.step_height - 1

    #Redondear para abajo?
    #Guardar posicion ?

    for step in range(self.parameter):
      query = "SELECT {column} FROM {data_table} ORDER BY {column} LIMIT 1 OFFSET {offset} ".format(
        column=self.column, data_table=self.table, offset=offset)

      attribute = c.execute(query).fetchone()[0]

      self.steps.append(attribute)
      offset += self.step_height

    conn.commit()
    conn.close()

  def estimate_equal(self, value):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    step_percentage = 1.0 / self.parameter

    beans_in = 0
    if value < self.min_value or value > self.max_value:
      estimator = 0
    else:
      if value == self.min_value:
        beans_in += 1
      for i, val in enumerate(self.steps[1:]):
        # Encontrar el bean donde se encuentra value
        if (value > self.steps[i] and value <= self.steps[i+1]) or (value == self.steps[i] and value == self.steps[i+1]):
          beans_in += 1

    return (self.step_height * beans_in) / self.total_elem



  # TODO: no se usa la altura en ningun lado?
  def estimate_lower(self, value):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    table_name = "steps_{colum}".format(colum=self.column)
    step_percentage = 1.0 / self.parameter

    if value < self.min_value:
      estimator = 0
    elif value > self.max_value:
      estimator = 1
    elif value in self.steps:
      # Obtener el indice del ultimo elemento == value
      step = len(self.steps) - self.steps[::-1].index(value) - 1
      estimator = step_percentage * (step + 1)
    else:
      for i, val in enumerate(self.steps):
        # Encontrar el bean donde se encuentra value
        if value < val:
          next_border = val
          break

      next_step = self.steps.index(next_border)
      next_estimator = step_percentage * (next_step + 1)
      prev_step = next_step - 1
      prev_estimator = step_percentage * (prev_step + 1)
      estimator = (next_estimator + prev_estimator) / 2

    return estimator

  def estimate_greater(self, value):
    return 1 - self.estimate_lower(value)

