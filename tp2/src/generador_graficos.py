# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


# Classic
x = [-3, 0, 3, 6, 9]

k=[1,2,13,3,1]

ax = plt.subplot(111)
plt.xticks([-3, 0, 3, 6, 9,12])
ax.bar(x, k, width=3, color='r',align='edge')
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

plt.show()


# Step
bx = plt.subplot(111)
x = [0,1,2,3,4]

k=[5,5,5,5,0]
labels = ['0', '4', '4', '4', '12']
plt.xticks(x, labels)
bx.bar(x, k, width=1, color='r',align='edge')
plt.axis([0, 6, 0, 8])
plt.yticks([0,1,2,3,4,5,6,7,8])

plt.show()



