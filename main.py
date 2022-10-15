import csv

import matplotlib.pyplot as plt

with open('data.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))


# filter only first two columns
data = [row[:2] for row in data]

#remove first character from each element
data = [[row[0][1:], row[1][1:]] for row in data]

#convert to float
data = [[float(row[0]), float(row[1])] for row in data]

# plot data as scatter plot with cross markers
plt.scatter([row[0] for row in data], [row[1] for row in data], marker='x')
# add labels
plt.xlabel(r'd in $[m]$')
plt.ylabel(r'N in $[\frac{1}{60s}]$')
# scale y axis logarithmic
plt.savefig('plot_1.pdf')
plt.yscale('log')
# save plot as pdf
plt.savefig('plot_2.pdf')
plt.show()


print(data)
