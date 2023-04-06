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

# read dataHd from csv file
with open('dataHd.csv', newline='') as csvfile:
    dataHd = list(csv.reader(csvfile))

# read dataNd from csv file
with open('dataNd.csv', newline='') as csvfile:
    dataNd = list(csv.reader(csvfile))

# convert to float
dataNd = [[float(row[0]), float(row[1])] for row in dataNd]
dataHd = [[float(row[0]), float(row[1])] for row in dataHd]

# convert to the correct units (Celsius to Kelvin)
# calculate the inversion of the temperature (1/T)
for i in range(len(dataNd)):
    dataNd[i][0] = dataNd[i][0] + 273.15
    dataNd[i][0] = dataNd[i][0] ** -1

# calculate the quotient of p and p_0
# calculate the logarithm of the quotient
for i in range(len(dataNd)):
    dataNd[i][1] = dataNd[i][1] / 1009
    dataNd[i][1] = np.log(dataNd[i][1])

# convert to the correct units (Celsius to Kelvin)
for i in range(len(dataHd)):
    dataHd[i][1] = dataHd[i][1] + 273.15

# swap x and y values (Hd)
dataHd = [[float(row[1]), float(row[0])] for row in dataHd]

# define universal gas constant and A etc.
R = 8.314
A = 0.9
N = 6.022 * 10 ** 23
eV = 1.602176634 * 10 ** -19
L_l = 4.08 * 10 ** 4

# plot dataNd as scatter plot with small dots
plt.scatter([row[0] for row in dataNd], [row[1] for row in dataNd], marker='.', s=1)

# linear regression for Nd
slope, intercept, r_value, p_value, std_err = sp.stats.linregress([row[0] for row in dataNd],
                                                                  [row[1] for row in dataNd])

# plot linear regression for Nd
plt.plot([0, 0.0035], [intercept, slope * 0.0035 + intercept], color='orange')

# adjust plot (Limits, Labels, Legend)
plt.xlim(0.0026, 0.0035)
plt.ylim(-4, 0)
plt.legend(['Messwerte', 'Ausgleichsgerade'])
plt.xlabel(r'$\frac{1}{T}$ in $\si{\per\kelvin}$')
plt.ylabel(r'$\ln\left(\frac{p}{p_0}\right)$')
plt.savefig('plots/plot_1.png', dpi=1920 / 8)

print(slope, std_err)
result = sp.stats.linregress([row[0] for row in dataNd], [row[1] for row in dataNd])
print(result.intercept, result.intercept_stderr)

latex('m', slope, std_err, '\kelvin', 0, 3)
latex('n', intercept, result.intercept_stderr, '', 0, 3)
m = ufloat(slope, std_err)
L = -1 * m * R
latex('L', L.n, L.s, '\joule\per\mole', 4, 3)

L_a = ufloat(3101.122, 0)

L_i = L - L_a

latex('L_i', L_i.n, L_i.s, '\joule\per\mole', 4, 3)

L_i_e = (L_i / N) / eV
latex('L_i_e', L_i_e.n, L_i_e.s, '\electronvolt', 0, 3)

k = 1- (L_i / L_l)
latex('k', k.n, k.s, '', -2, 3)



plt.clf()

# plot dataHd as scatter plot with dots
plt.scatter([row[0] for row in dataHd], [row[1] for row in dataHd], marker='.')

# values for x and y
T = [row[0] for row in dataHd]
p = [row[1] for row in dataHd]


# Ausgleichsfunktion
def func(x, a, b, c, d):
    return a * x ** 3 + b * x ** 2 + c * x + d


def dfunc(x, a, b, c):
    return 3 * a * x ** 2 + 2 * b * x + c


para, pcov = curve_fit(func, T, p)
a, b, c, d = para
xx = np.linspace(0, 500, 1000)
plt.plot(xx, func(xx, a, b, c, d), color='orange')

# adjust plot (Limits, Labels, Legend)
plt.xlim(380, 480)
plt.ylim(0, 15)
plt.legend(['Messwerte', 'Ausgleichspolynom'])
plt.xlabel(r'$T$ in $\si{\kelvin}$')
plt.ylabel(r'$p$ in $\SI{e5}{\pascal}$')
plt.savefig('plots/plot_2.png', dpi=1920 / 8)

latex('a', a, np.sqrt(pcov[0][0]), '\pascal\per\kelvin\\tothe{3}', -6, 3)
latex('b', b, np.sqrt(pcov[1][1]), '\pascal\per\kelvin\\tothe{2}', -3, 3)
latex('c', c, np.sqrt(pcov[2][2]), '\pascal\per\kelvin', 0, 3)
latex('d', d, np.sqrt(pcov[3][3]), '\pascal', 2, 3)

plt.clf()


def v_plus(T, p):
    return (R * T) / (2 * p) + np.sqrt((R ** 2 * T ** 2) / (4 * p ** 2) - (A / p))


def v_minus(T, p):
    return (R * T) / (2 * p) - np.sqrt((R ** 2 * T ** 2) / (4 * p ** 2) - (A / p))


def l_plus(T):
    return v_plus(T, func(T, a, b, c, d)) * T * dfunc(T, a, b, c)


def l_minus(T):
    return v_minus(T, func(T, a, b, c, d)) * T * dfunc(T, a, b, c)


Tlin = np.linspace(380, 480, 100)

plt.plot(Tlin, l_plus(Tlin), color='orange')
plt.xlim(380, 480)
plt.xlabel(r'$T$ in $\si{\kelvin}$')
plt.ylabel(r'$L$ in $\SI{}{\J\per\mol}$')
plt.savefig('plots/plot_plus.png', dpi=1920 / 8)

plt.clf()

plt.plot(Tlin, l_minus(Tlin), color='orange')
plt.xlim(380, 480)
plt.xlabel(r'$T$ in $\si{\kelvin}$')
plt.ylabel(r'$L$ in $\SI{}{\J\per\mol}$')
plt.savefig('plots/plot_minus.png', dpi=1920 / 8)

# a & = \SI{0(0)e4}{\pascal\per\K^3}\
