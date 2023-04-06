import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.optimize import curve_fit
from uncertainties import ufloat

# import usepackage siunitx
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx} \sisetup{per-mode=fraction, exponent-product = \cdot, '
                              r'separate-uncertainty = true, output-decimal-marker = {,}}')
def latex(w_name, w, w_err, w_unit, magnitude, digits):
    print(w_name, '&=', '\SI{', round(w / (10 ** magnitude), digits), '(', round(w_err / (10 ** magnitude), digits),
          ')e', magnitude, '}{', w_unit, '}')

# read data
with open('dataWithoutNoise.csv', newline='') as csvfile:
    dataWithoutNoise = list(csv.reader(csvfile))

with open('dataWithNoise.csv', newline='') as csvfile:
    dataWithNoise = list(csv.reader(csvfile))

with open('dataLed.csv', newline='') as csvfile:
    dataLed = list(csv.reader(csvfile))

with open('dataLedGemogelt.csv', newline='') as csvfile:
    dataLedGemogelt = list(csv.reader(csvfile))

# convert data to float
dataWithoutNoise = [[float(x) for x in row] for row in dataWithoutNoise]
dataWithNoise = [[float(x) for x in row] for row in dataWithNoise]
dataLed = [[float(x) for x in row] for row in dataLed]
dataLedGemogelt = [[float(x) for x in row] for row in dataLedGemogelt]

# covert grad to rad
dataWithoutNoise = [[x[0] * np.pi / 180, x[1]] for x in dataWithoutNoise]
dataWithNoise = [[x[0] * np.pi / 180, x[1]] for x in dataWithNoise]

def func(phi, U_0, a, b):
    return (2/np.pi) * U_0 * np.cos(phi - a) + b

# plot dataWithoutNoise
plt.plot([x[0] for x in dataWithoutNoise], [x[1] for x in dataWithoutNoise], 'gx', label='Messwerte ohne Rauschen')
ticks = [0,np.pi/2,np.pi,(3/2)*np.pi,2*np.pi]
labels = [0,r'$\frac{1}{2}\pi$', r'$\pi$', r'$\frac{3}{2}\pi$',r'$2\pi$']
plt.xticks(ticks, labels)

x = [row[0] for row in dataWithoutNoise]
y = [row[1] for row in dataWithoutNoise]

para, pcov = curve_fit(func, x, y)
U_0, a, b = para
xx = np.linspace(0, 2*np.pi, 1000)
plt.plot(xx, func(xx, U_0, a, b), color='red', label='Ausgleichskurve')

print('Ohne Rauschen')

# print parameters
print('U_0 =', U_0)
print('a =', a)
print('b =', b)

# print std error of parameters
print('U_0_err =', np.sqrt(pcov[0][0]))
print('a_err =', np.sqrt(pcov[1][1]))
print('b_err =', np.sqrt(pcov[2][2]))


# save plot
plt.xlabel(r'$\phi$ / rad')
plt.ylabel(r'$U$ / mV')
plt.legend(loc='best')
plt.savefig('plots/plotWithoutNoise.pdf')
plt.clf()

# plot dataWithNoise
plt.plot([x[0] for x in dataWithNoise], [x[1] for x in dataWithNoise], 'gx', label='Messwerte mit Rauschen')
ticks = [0,np.pi/2,np.pi,(3/2)*np.pi,2*np.pi]
labels = [0,r'$\frac{1}{2}\pi$', r'$\pi$', r'$\frac{3}{2}\pi$',r'$2\pi$']
plt.xticks(ticks, labels)

x = [row[0] for row in dataWithNoise]
y = [row[1] for row in dataWithNoise]

para, pcov = curve_fit(func, x, y)
U_0, a, b = para
xx = np.linspace(0, 2*np.pi, 1000)
plt.plot(xx, func(xx, U_0, a, b), color='red', label='Ausgleichskurve')

print('Mit Rauschen')

# print parameters
print('U_0 =', U_0)
print('a =', a)
print('b =', b)

# print std error of parameters
print('U_0_err =', np.sqrt(pcov[0][0]))
print('a_err =', np.sqrt(pcov[1][1]))
print('b_err =', np.sqrt(pcov[2][2]))

# save plot
plt.xlabel(r'$\phi$ / rad')
plt.ylabel(r'$U$ / mV')
plt.legend(loc='best')
plt.savefig('plots/plotWithNoise.pdf')
plt.clf()

def distance(r, a, b):
    return (a/r**2) + b

# plot dataLed
plt.plot([x[0] for x in dataLedGemogelt], [x[1] for x in dataLedGemogelt], 'gx', label='Messwerte mit LED')

x = [row[0] for row in dataLedGemogelt]
y = [row[1] for row in dataLedGemogelt]

para, pcov = curve_fit(distance, x, y)
a, b = para
xx = np.linspace(5, 160, 1000)
plt.plot(xx, distance(xx, a, b), color='red', label='Ausgleichskurve')

print('Mit LED gemogelt')

# print parameters
print('a =', a)
print('b =', b)

# print std error of parameters
print('a_err =', np.sqrt(pcov[0][0]))
print('b_err =', np.sqrt(pcov[1][1]))

# save plot
plt.xlim(0, 150)
plt.ylim(0, 10000)
plt.xlabel(r'$r$ / cm')
plt.ylabel(r'$U$ / mV')
plt.legend(loc='best')
plt.savefig('plots/plotLedGemogelt.pdf')
plt.clf()

# plot dataLed
plt.plot([x[0] for x in dataLed], [x[1] for x in dataLed], 'gx', label='Messwerte mit LED')

x = [row[0] for row in dataLed]
y = [row[1] for row in dataLed]

para, pcov = curve_fit(distance, x, y)
a, b = para
xx = np.linspace(5, 160, 1000)
plt.plot(xx, distance(xx, a, b), color='red', label='Ausgleichskurve')

print('Mit LED')

# print parameters
print('a =', a)
print('b =', b)

# print std error of parameters
print('a_err =', np.sqrt(pcov[0][0]))
print('b_err =', np.sqrt(pcov[1][1]))

# save plot
plt.xlim(0, 150)
plt.ylim(0, 10000)
plt.xlabel(r'$r$ / cm')
plt.ylabel(r'$U$ / mV')
plt.legend(loc='best')
plt.savefig('plots/plotLed.pdf')
plt.clf()