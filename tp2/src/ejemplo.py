# -*- coding: utf-8 -*-
from distribution_steps import DistributionSteps
from classic_histogram import ClassicHistogram
from real_histogram import RealHistogram

# Creo una instancia de la clase que representa al metodo
# 'Histograma Clasico'
aEstimator = ClassicHistogram('db.sqlite3', 'table1', 'c1', parameter=20)

# Pruebo distintas instancias de estimacion
print "Classic Histogram"
print "  Sel(=%d) : %3.2f" % (50, aEstimator.estimate_equal(50))
print "  Sel(>%d) : %3.2f" % (70, aEstimator.estimate_greater(70))

