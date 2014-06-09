# -*- coding: utf-8 -*-
import classic_histogram
import sqlite3
import numpy as np
import pylab
import random
import math

class RealHistogram(classic_histogram.ClassicHistogram):
  """Histograma real."""

  def build_struct(self):
    conn = sqlite3.connect(self.db)
    c = conn.cursor()

    # Hago lo mismo que el classic pero con un salto de 1
    self.min_value, self.max_value, self.total_elem = c.execute(
        "SELECT min({0}), max({0}), count(*) FROM {1}".format(self.column, self.table)).fetchone()
    bucket = 1
    prev_value = self.min_value
    next_value = prev_value
    total = 0
    self.borders = {}

    while total != self.total_elem:
      a = "SELECT count(*) FROM {0} where {1} = {2}".format(self.table, self.column, next_value)

      amount = c.execute(a).fetchone()[0]
      total += amount
      self.borders[next_value] = {'amount': amount, 'cumulative': total}
      prev_value = next_value
      next_value += bucket

    conn.commit()
    conn.close()
