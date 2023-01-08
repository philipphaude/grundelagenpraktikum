import csv
import matplotlib.pyplot as plt
import scipy.stats as stats

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')


#read data from csv file
with open('data.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))


#convert to float
data = [[float(row[0]), float(row[1])] for row in data]

# divide y values by 5
data = [[row[0], row[1]/5] for row in data]

# divide x values by 100
data = [[row[0]/100, row[1]] for row in data]

# square x values
data = [[row[0]**2, row[1]] for row in data]

# square y values
data = [[row[0], row[1]**2] for row in data]



#plot data as scatter plot with cross markers
plt.scatter([row[0] for row in data], [row[1] for row in data], marker='x')
plt.ylabel(r'$T^2$ in $\SI{}{\s^2}$')
plt.xlabel(r'$a^2$ in $\SI{}{\m^2}$')

# linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress([row[0] for row in data], [row[1] for row in data])
plt.plot([0, 550/10000], [intercept, slope*550/10000+intercept], color='orange')
plt.xlim(0, 550/10000)
plt.ylim(0, 45)
print(slope, std_err)

result = stats.linregress([row[0] for row in data], [row[1] for row in data])
print(result.intercept, result.intercept_stderr)


#legend
plt.legend(['Messwerte', 'Ausgleichsgerade'])


plt.savefig('plot_2.png', dpi=1920/8)



