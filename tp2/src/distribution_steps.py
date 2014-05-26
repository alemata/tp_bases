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
    table_name = "steps_{colum}".format(colum=self.column)
    c.execute(
      "CREATE TABLE IF NOT EXISTS {table_name} (step integer, {column} integer, step_height integer)".format(
        table_name=table_name, column=self.column))
    c.execute("DELETE FROM {table_name}".format(table_name=table_name))

    min_value, max_value, total_elem = c.execute(
      "SELECT min({0}), max({0}), count(*) FROM {1}".format(self.column, self.table)).fetchone()
    step_height = math.floor(total_elem / self.parameter)

    offset = step_height - 1

    #Redondear para abajo?
    #Guardar posicion ?

    for step in range(self.parameter):
      query = "SELECT {column} FROM {data_table} ORDER BY {column} LIMIT 1 OFFSET {offset} ".format(
        column=self.column, data_table=self.table, offset=offset)

      attribute = c.execute(query).fetchone()[0]
      a = "INSERT INTO {table_name} VALUES ({step}, {attribute}, {step_height})".format(table_name=table_name,
                                                                                        step=step,
                                                                                        attribute=attribute,
                                                                                        step_height=step_height)
      c.execute(a)
      offset += step_height

    conn.commit()
    conn.close()
    print "----------Finalizada la creacion de la estructura----------------"

  def estimate_equal(self, value):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    table_name = "steps_{colum}".format(colum=self.column)

    # # Calcular total de elementos de la tabla
    # total_elem = "select cumulative from {0} order by cumulative DESC limit 1".format(table_name)
    # total = c.execute(total_elem).fetchone()[0]
    #
    # # Si es un borde entonces busco el valor directamente
    # borders = c.execute("select border from {0}".format(table_name)).fetchall()
    # if (value,) in borders:
    #     a = "SELECT amount FROM {0} where border = {1}".format(table_name, value)
    #     amount = c.execute(a).fetchone()[0]
    #     estimator = (amount / float(total))
    #     print "El estimador de {0} es: {1}".format(value, estimator)
    # else:
    #     for i, val in enumerate(borders):
    #         # Encontrar el bean donde se encuentra value
    #         if value < val[0]:
    #             border = val[0]
    #             break
    #     a = "SELECT amount FROM {0} where border = {1}".format(table_name, border)
    #     amount = c.execute(a).fetchone()[0]
    #     estimator = (amount / float(total))
    #     print "El estimador de {0} es: {1}".format(value, estimator)
    #
    # return estimator

  def estimate_lower(self, value):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    table_name = "steps_{colum}".format(colum=self.column)
    step_percentage = 1.0 / self.parameter

    borders = c.execute(
      "select {column} from {table_name} ORDER BY {column}".format(column=self.column,
                                                                   table_name=table_name)).fetchall()

    if (value,) in borders:
      a = "SELECT step FROM {table_name} where {column} = {border} ORDER BY step DESC LIMIT 1".format(
        table_name=table_name, border=value, column=self.column)
      step = c.execute(a).fetchone()[0]
      estimator = step_percentage * (step + 1)
    else:
      for i, val in enumerate(borders):
        # Encontrar el bean donde se encuentra value
        if value < val[0]:
          next_border = val[0]
          break

      a = "SELECT step FROM {table_name} where {column} = {border} ORDER BY step LIMIT 1".format(
        table_name=table_name, border=next_border, column=self.column)
      next_step = c.execute(a).fetchone()[0]
      next_estimator = step_percentage * (next_step + 1)
      prev_step = next_step - 1
      prev_estimator = step_percentage * (prev_step + 1)
      estimator = (next_estimator + prev_estimator) / 2

    print "El estimador de {0} es: {1}".format(value, estimator)
    return estimator

  def estimate_greater(self, value):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()
    table_name = "steps_{colum}".format(colum=self.column)

