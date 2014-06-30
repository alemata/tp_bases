# -*- coding: utf-8 -*-
from openpyxl import load_workbook 
wb2 = load_workbook('fechas_nacimiento.xltx')

ws4 = wb2.get_sheet_by_name(wb2.get_sheet_names()[0])

days = []
for row in ws4.range('A2:A367'):
  for cell in row:
    days.append(cell.value)

amounts = []
for row in ws4.range('B2:B367'):
  for cell in row:
    amounts.append(cell.value)


import matplotlib.pyplot as plt
from numpy.random import normal
plt.plot(days, amounts)
plt.xlabel("Numero de dia")
plt.ylabel("Cantidad de nacimientos")
plt.show()
