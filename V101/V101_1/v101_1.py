import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')


#read data from csv file
with open('data.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

    #swap x and y values
    data = [[float(row[1]), float(row[0])] for row in data]


#convert to float
data = [[float(row[0]), float(row[1])] for row in data]

# multiply y values by 20
data = [[row[0], row[1]*20] for row in data]

# x values divided by 180 and multiply by pi
data = [[row[0]/180*np.pi, row[1]] for row in data]


#plot data as scatter plot with cross markers
plt.scatter([row[0] for row in data], [row[1] for row in data], marker='x')
plt.ylabel(r'M in $[\SI{}{\N\centi\m}]$')
plt.xlabel(r'$\varphi$ in [Rad]')


#polyfit
slope, intercept, r_value, p_value, std_err = stats.linregress([row[0] for row in data], [row[1] for row in data])
plt.plot([0, 3.5], [intercept, slope*3.5+intercept], color='orange')
plt.xlim(0, 3.5)
plt.ylim(0, 6.5)

#legend
plt.legend(['Messwerte', 'Ausgleichsgerade'])

#print slope and intercept
print(slope, std_err)

result = stats.linregress([row[0] for row in data], [row[1] for row in data])
print(result.intercept, result.intercept_stderr)




plt.savefig('../plots/plot_1.png', dpi=1920/8)
plt.show()



