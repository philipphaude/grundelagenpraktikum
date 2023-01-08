import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')


#read data from csv file
with open('table-1.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))



#convert to float
for i in range(len(data)):
    for j in range(len(data[i])):
        data[i][j] = float(data[i][j])

# divide all data by 5
for i in range(len(data)):
    for j in range(len(data[i])):
        data[i][j] = data[i][j]/5



#show data
print(data)

# print average of x values and y values and their standard deviation and error
print('Kugel average: ', np.mean([row[0] for row in data]))
print('Kugel error: ', stats.sem([row[0] for row in data]))
print('Zylinder average: ', np.mean([row[1] for row in data]))
print('Zylinder error: ', stats.sem([row[1] for row in data]))
print('Puppe 1 average: ', np.mean([row[2] for row in data]))
print('Puppe 1 error: ', stats.sem([row[2] for row in data]))
print('Puppe 2 average: ', np.mean([row[3] for row in data]))
print('Puppe 2 error: ', stats.sem([row[3] for row in data]))