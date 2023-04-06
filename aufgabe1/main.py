import csv
import matplotlib.pyplot as plt

with open('data.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

# filter only first two columns
data = [row[:2] for row in data]

# remove first character from each element
data = [[row[0][1:], row[1][1:]] for row in data]

# convert to float
data = [[float(row[0]), float(row[1])] for row in data]

# plot data as scatter plot with cross markers
plt.scatter([row[0] for row in data], [row[1] for row in data], marker='x')
plt.xlabel(r'd in $[cm]$')
plt.ylabel(r'N in $[\frac{1}{60s}]$')
plt.savefig('plots/plot_1.png', dpi=1920/8)
plt.yscale('log')
# save plot as png 1080p
plt.savefig('plots/plot_2.png', dpi=1920/8)
