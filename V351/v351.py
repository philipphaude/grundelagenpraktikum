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


def saegeF(x, n):
    value = 0
    for k in range(1, n + 1):
        value += ((-1) ** (k + 1)) * (np.sin(k * x) / k)

    return -2 * value


def rechtF(x, n):
    value = 0
    for k in range(1, n + 1):
        value += np.sin((2 * k - 1) * x) / (2 * k - 1)

    return (4 / np.pi) * value


def dreiF(x, n):
    value = 0
    for k in range(1, n + 1):
        value += (np.cos((2 * k - 1) * x) / (2 * k - 1) ** 2)

    return (np.pi / 2) - (4 / np.pi) * value


# plot saegeF
x = np.linspace(0, 2 * np.pi, 1000)
plt.plot(x, saegeF(x, 1), label='n = 1')
plt.plot(x, saegeF(x, 2), label='n = 2')
plt.plot(x, saegeF(x, 5), label='n = 5')
plt.plot(x, saegeF(x, 20), label='n = 20')
plt.xlim(0, 2 * np.pi)
plt.legend()
plt.xlabel(r'$x$')
plt.ylabel(r'$f(x)$')
plt.savefig('plots/sägezahn.pdf')
plt.clf()

# plot rechtF
plt.plot(x, rechtF(x, 1), label='n = 1')
plt.plot(x, rechtF(x, 2), label='n = 2')
plt.plot(x, rechtF(x, 5), label='n = 5')
plt.plot(x, rechtF(x, 20), label='n = 20')
plt.xlim(0, 2 * np.pi)
plt.legend()
plt.xlabel(r'$x$')
plt.ylabel(r'$f(x)$')
plt.savefig('plots/rechteck.pdf')
plt.clf()

# plot dreiF
x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
plt.plot(x, dreiF(x, 1), label='n = 1')
plt.plot(x, dreiF(x, 2), label='n = 2')
plt.plot(x, dreiF(x, 5), label='n = 5')
plt.plot(x, dreiF(x, 20), label='n = 20')
plt.xlim(-2 * np.pi, 2 * np.pi)
plt.legend()
plt.xlabel(r'$x$')
plt.ylabel(r'$f(x)$')
plt.savefig('plots/dreiecks.pdf')
plt.clf()


# read data
with open('dreieck.csv', newline='') as csvfile:
    dreieck = list(csv.reader(csvfile))

with open('rechteck.csv', newline='') as csvfile:
    rechteck = list(csv.reader(csvfile))

with open('saegezahn.csv', newline='') as csvfile:
    saegezahn = list(csv.reader(csvfile))

# convert data to float
dreieck = [[float(x) for x in row] for row in dreieck]
rechteck = [[float(x) for x in row] for row in rechteck]
saegezahn = [[float(x) for x in row] for row in saegezahn]

# convert data from dB to V
dreieck = [[x[0], (10 ** (x[1] / 20)) * 0.775] for x in dreieck]
rechteck = [[x[0], (10 ** (x[1] / 20)) * 0.775] for x in rechteck]
saegezahn = [[x[0], (10 ** (x[1] / 20)) * 0.775] for x in saegezahn]

def func(x, a, b):
    return a * x ** b


# plot data dreieck
plt.plot([x[0] for x in dreieck], [x[1] for x in dreieck], 'gx', label='Messwerte Dreieck')

para, pcov = curve_fit(func, [row[0] for row in dreieck] , [row[1] for row in dreieck])
a, b = para
xx = np.linspace(1, 140, 1000)
plt.plot(xx, func(xx, a, b), color='red', label='Ausgleichskurve')

#print error of a
print('Dreieck:')
print('a =', a, 'pm', np.sqrt(pcov[0][0]))
print('b =', b, 'pm', np.sqrt(pcov[1][1]))
c = ((b + 2) / - 2) * 100
print('c =', c, 'pm', np.sqrt(pcov[1][1]))

plt.xlabel(r'$\nu \:/\: \si{\hertz}$')
plt.ylabel(r'$U \:/\: \si{\volt}$')
plt.xlim(-5, 140)
plt.ylim(-0.2, 2.5)
plt.legend(loc='best')
plt.savefig('plots/dreieckA.pdf')
plt.clf()

# plot data rechteck
plt.plot([x[0] for x in rechteck], [x[1] for x in rechteck], 'gx', label='Messwerte Rechteck')

para, pcov = curve_fit(func, [row[0] for row in rechteck] , [row[1] for row in rechteck])
a, b = para
xx = np.linspace(1, 200, 1000)
plt.plot(xx, func(xx, a, b), color='red', label='Ausgleichskurve')

#print error of a
print('Rechteck:')
print('a =', a, 'pm', np.sqrt(pcov[0][0]))
print('b =', b, 'pm', np.sqrt(pcov[1][1]))
c = ((b + 1) / - 1) * -100
print('c =', c, 'pm', np.sqrt(pcov[1][1]))

plt.xlabel(r'$\nu \:/\: \si{\hertz}$')
plt.ylabel(r'$U \:/\: \si{\volt}$')
plt.ylim(0, 4)
plt.xlim(0, 200)
plt.legend(loc='best')
plt.savefig('plots/rechteckA.pdf')
plt.clf()

# plot data saegezahn
plt.plot([x[0] for x in saegezahn], [x[1] for x in saegezahn], 'gx', label='Messwerte Sägezahn')

para, pcov = curve_fit(func, [row[0] for row in saegezahn] , [row[1] for row in saegezahn])
a, b = para
xx = np.linspace(1, 200, 1000)
plt.plot(xx, func(xx, a, b), color='red', label='Ausgleichskurve')

#print error of a
print('Sägezahn:')
print('a =', a, 'pm', np.sqrt(pcov[0][0]))
print('b =', b, 'pm', np.sqrt(pcov[1][1]))
c = ((b + 1) / -1) * -100
print('c =', c, 'pm', np.sqrt(pcov[1][1]))

plt.xlabel(r'$\nu \:/\: \si{\hertz}$')
plt.ylabel(r'$U \:/\: \si{\volt}$')
plt.ylim(0, 2)
plt.xlim(0, 100)
plt.legend(loc='best')
plt.savefig('plots/saegezahnA.pdf')
plt.clf()
