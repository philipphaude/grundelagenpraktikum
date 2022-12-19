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
with open('dataKleine.csv', newline='') as csvfile:
    dataKleine = list(csv.reader(csvfile))

with open('dataGroß.csv', newline='') as csvfile:
    dataGroß = list(csv.reader(csvfile))

with open('dataTemp.csv', newline='') as csvfile:
    dataTemp = list(csv.reader(csvfile))

# convert dataKleine to float
dataKleine = [[float(x) for x in row] for row in dataKleine]
dataGroß = [[float(x) for x in row] for row in dataGroß]

# convert dataTemp to float
dataTemp = [[float(x) for x in row] for row in dataTemp]

# convert to the correct units (Celsius to Kelvin)
dataTemp = [[x[0] + 273.15, x[1], x[2], x[3], x[4]] for x in dataTemp]



dataKleineAve = 0
dataGroßAve = 0
# for loop to sum up dataKleine
for i in range(0, 10):
    dataKleineAve = dataKleineAve + dataKleine[i][0]
    dataGroßAve = dataGroßAve + dataGroß[i][0]

dataKleineAve = dataKleineAve / 10
dataGroßAve = dataGroßAve / 10

m_kl = ufloat(4.45, 0.01)
m_kl = m_kl * 10 ** -3

m_gr = ufloat(4.6, 0.01)
m_gr = m_gr * 10 ** -3

d_kl = ufloat(15.05, 0.01)
d_kl = d_kl * 10 ** -3

d_gr = ufloat(15.25, 0.01)
d_gr = d_gr * 10 ** -3

r_kl = d_kl / 2
r_gr = d_gr / 2

V_kl = 4 / 3 * np.pi * r_kl ** 3
V_gr = 4 / 3 * np.pi * r_gr ** 3

p_kl = m_kl / V_kl
p_gr = m_gr / V_gr

K_kl = ufloat(0.07640 * 10 ** -3, 0)

p_Wasser = ufloat(997, 0)

eta_0 = K_kl * (p_kl - p_Wasser) * dataKleineAve

K_gr = eta_0 / ((p_gr - p_Wasser) * dataGroßAve)

print(dataTemp)

v_t = dataTemp[0][0] / ((dataTemp[0][1] + dataTemp[0][2] + dataTemp[0][3] + dataTemp[0][4])/4)
v_h = dataTemp[-1][0] / ((dataTemp[-1][1] + dataTemp[-1][2] + dataTemp[-1][3] + dataTemp[-1][4])/4)

Re_t = v_t * p_Wasser * d_gr / eta_0
Re_h = v_h * p_Wasser * d_gr / eta_0

# first row of dataTemp = 1/Temp
dataTemp = [[1 / x[0], K_gr * (p_gr - p_Wasser) * x[1], K_gr * (p_gr - p_Wasser) * x[2], K_gr * (p_gr - p_Wasser) * x[3], K_gr * (p_gr - p_Wasser) * x[4]] for x in dataTemp]

dataTemp = [[x[0], (x[1]+x[2]+x[3]+x[4])/4 ] for x in dataTemp]




# plot dots dataTemp without error bars with nominal values
plt.plot([x[0] for x in dataTemp], [np.log(x[1].nominal_value) for x in dataTemp], 'o', label=r'Messdaten')

# linear fit dataTemp
slope, intercept, r_value, p_value, std_err = sp.stats.linregress([row[0] for row in dataTemp], [np.log(row[1].nominal_value) for row in dataTemp])

result = sp.stats.linregress([row[0] for row in dataTemp], [np.log(row[1].nominal_value) for row in dataTemp])
print(result.intercept, result.intercept_stderr)

# plot linear regression for Nd
plt.plot([0, 0.05], [intercept, slope * 0.05 + intercept], color='orange', label=r'lineare Regression')

plt.xlim(0.00305, 0.0034)
plt.ylim(-0.2, 0.35)

plt.xlabel(r'$\frac{1}{T}$ in $\si{\per\kelvin}$')
plt.ylabel(r'$\ln(\eta)$')

plt.legend(loc='best')


#save plot
plt.savefig('plotTemp.pdf')

m = ufloat(slope, std_err)
n = ufloat(intercept, result.intercept_stderr)

A = np.e**n
B = m


print('Durchschnittliche Zeit klein', dataKleineAve)
print('Durchschnittliche Zeit groß', dataGroßAve)
latex('Dichte Kleine Kugel', p_kl.n, p_kl.s, 'kg/m^3', 0, 3)
latex('Dichte Große Kugel', p_gr.n, p_gr.s, 'kg/m^3', 0, 3)
latex('Viskosität Kleine Kugel', eta_0.n, eta_0.s, 'Pas', 0, 3)
latex('Aparaturkonstante Große Kugel', K_gr.n, K_gr.s, 'Pas', -5, 3)
latex('Steigung', slope, std_err, '1/kelvin', 0, 3)
latex('y-Achsenabschnitt', result.intercept, result.intercept_stderr, 'ln(Pas)', 0, 3)
latex('A', A.n, A.s, 'Pas', -3, 3)
latex('B', B.n, B.s, 'kelvin', 0, 3)
latex('Reynoldszahl tief', Re_t.n, Re_t.s, '', 0, 3)
latex('Reynoldszahl hoch', Re_h.n, Re_h.s, '', 0, 3)

print(dataTemp)
