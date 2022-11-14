import csv
import matplotlib.pyplot as plt
import numpy as np

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')

with open('data.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
print(data)
# import latex usepackage siunitx matplotlibrc
# https://matplotlib.org/3.1.1/tutorials/text/mathtext.html

# convert to float
data = [[float(row[0]), float(row[1])] for row in data]

plt.scatter([row[0] for row in data], [row[1] for row in data], marker='x', color='black')
m, b = np.polyfit([row[0] for row in data], [row[1] for row in data], 1)
plt.plot([0, 55], [b, m*55+b], color='orange')

plt.xlim(0, 55)
plt.ylim(0, 1.7)
plt.xlabel(r'$\Delta x$ in $[\SI{}{\centi\meter}]$')
plt.ylabel(r'F in $[\SI{}{\newton}]$')
plt.savefig('plot_1.png', dpi=1920/8)