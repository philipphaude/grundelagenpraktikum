import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from uncertainties import ufloat

plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')



#read data from csv file
with open('data.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

#convert data to float
data = [[float(x) for x in row] for row in data]

#Einheiten umrechnen
data = [[row[0]/100, row[1]/1000000, row[2]/1000000, row[3]/1000000, row[4]/1000000] for row in data]
#Hilfsgleichung
l = 0.54
data_e = [[(l*(row[0]**2)-(row[0]**3/3)), row[1], row[2], row[3], row[4]] for row in data]

#new array data_b
data_b = [[row[0], row[1], row[2], row[3], row[4]] for row in data]

l = 0.55
#for loop to define data_b
for i in range(0, 9):
    x = data_b[i][0]
    data_b[i][0] = 3*l**2*x-4*x**3

for i in range(9, 18):
    x = data_b[i][0]
    data_b[i][0] = 4*x**3-12*l*x**2+9*l**2*x-l**3






plt.scatter([row[0] for row in data_e[:-2]], [row[3] for row in data_e[:-2]], marker='x')
slope, intercept, r_value, p_value, std_err = stats.linregress([row[0] for row in data_e[:-2]], [row[3] for row in data_e[:-2]])
plt.plot([0, 0.1], [intercept, slope*0.1+intercept], color='red')
plt.xlim(0, 0.1)
plt.ylim(0, 0.00045)
plt.xlabel(r'$\left(Lx^2-\frac{x^3}{3}\right)$ in $\si{\m^3}$')
plt.ylabel(r'$D(x)$ in $\si{\meter}$')
plt.legend([r'Messwerte', r'Lineare Regression'], loc='upper left')
plt.savefig('plot_rund_ein.png', dpi=1920/8)

k_rund_ein = ufloat(slope, std_err)

plt.clf()

plt.scatter([row[0] for row in data_e[:-2]], [row[4] for row in data_e[:-2]], marker='x')
slope, intercept, r_value, p_value, std_err = stats.linregress([row[0] for row in data_e[:-2]], [row[4] for row in data_e[:-2]])
plt.plot([0, 0.1], [intercept, slope*0.1+intercept], color='red')
plt.xlim(0, 0.1)
plt.ylim(0, 0.00045)
plt.xlabel(r'$\left(Lx^2-\frac{x^3}{3}\right)$ in $\si{\m^3}$')
plt.ylabel(r'$D(x)$ in $\si{\meter}$')
plt.legend([r'Messwerte', r'Lineare Regression'], loc='upper left')
plt.savefig('plot_eck_ein.png', dpi=1920/8)

k_eck_ein = ufloat(slope, std_err)

plt.clf()

plt.scatter([row[0] for row in data_b], [row[1] for row in data_b], marker='x')
slope, intercept, r_value, p_value, std_err = stats.linregress([row[0] for row in data_b], [row[1] for row in data_b])
plt.plot([0, 0.175], [intercept, slope*0.175+intercept], color='red')
plt.xlim(0, 0.175)
plt.ylim(0, 0.00005)
plt.xlabel(r'$3 L^2 x-4 x^3$ in $\si{\m^3}$ für $0 \leq x \leq \frac{L}{2}$ und $4 x^3-12 L x^2+9 L^2 x-L^3$ in $\si{\m^3}$ für $\frac{L}{2} \leq x \leq L$')
plt.ylabel(r'$D(x)$ in $\si{\meter}$')
plt.legend([r'Messwerte', r'Lineare Regression'], loc='upper left')
plt.savefig('plot_rund_bei.png', dpi=1920/8)

k_rund_bei = ufloat(slope, std_err)

plt.clf()

plt.scatter([row[0] for row in data_b], [row[2] for row in data_b], marker='x')
slope, intercept, r_value, p_value, std_err = stats.linregress([row[0] for row in data_b], [row[2] for row in data_b])
plt.plot([0, 0.175], [intercept, slope*0.175+intercept], color='red')
plt.xlim(0, 0.175)
plt.ylim(0, 0.00003)
plt.xlabel(r'$3 L^2 x-4 x^3$ in $\si{\m^3}$ für $0 \leq x \leq \frac{L}{2}$ und $4 x^3-12 L x^2+9 L^2 x-L^3$ in $\si{\m^3}$ für $\frac{L}{2} \leq x \leq L$')
plt.ylabel(r'$D(x)$ in $\si{\meter}$')
plt.legend([r'Messwerte', r'Lineare Regression'], loc='upper left')
plt.savefig('plot_eck_bei.png', dpi=1920/8)

k_eck_bei = ufloat(slope, std_err)

plt.clf()

#new variable with uncertainties
m_e = ufloat(0.4995, 0.0001)
m_b = ufloat(1.021, 0.0001)
g = ufloat(9.81, 0)
d = ufloat(0.01, 0.00005)
I_q = (d**4/12)
I_r = ((np.pi*d**4)/64)

e_rund_ein = ((m_e*g)/(2*k_rund_ein*I_r))
e_eck_ein = ((m_e*g)/(2*k_eck_ein*I_q))
e_rund_bei = ((m_b*g)/(48*k_rund_bei*I_r))
e_eck_bei = ((m_b*g)/(48*k_eck_bei*I_q))

#print I
print('I_r =', I_r)
print('I_q =', I_q)


#print values in e 9 format with uncertainties
print('e_rund_ein =', e_rund_ein)
print('e_eck_ein =', e_eck_ein)
print('e_rund_bei =', e_rund_bei)
print('e_eck_bei =', e_eck_bei)

# sum of e_eck_bei and e_rund_bei and e_eck_ein and e_rund_ein
e_sum = (e_eck_bei + e_rund_bei + e_eck_ein + e_rund_ein)/4
print('e_sum =', e_sum)
print('e_sum =', e_sum.n)










