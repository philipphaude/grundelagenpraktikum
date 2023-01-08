import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.optimize import curve_fit
from uncertainties import ufloat


def latex(w_name, w, w_err, w_unit, magnitude, digits):
    print(w_name, '&=', '\SI{', round(w / (10 ** magnitude), digits), '(', round(w_err / (10 ** magnitude), digits),
          ')e', magnitude, '}{', w_unit, '}')

LR_10 = 239
LR_11 = 489.9
LC_15 = 652
LR_15 = 473
LC_1 = 660
LC_3 = 420
LR_17i = 93.65
LL_17i = 41.85
LR_17m = 93.65
LL_17m = 41.85

# read data
with open('dataAW10.csv', newline='') as csvfile:
    dataAW10 = list(csv.reader(csvfile))

with open('dataAW11.csv', newline='') as csvfile:
    dataAW11 = list(csv.reader(csvfile))

with open('dataBW1.csv', newline='') as csvfile:
    dataBW1 = list(csv.reader(csvfile))

with open('dataBW3.csv', newline='') as csvfile:
    dataBW3 = list(csv.reader(csvfile))

with open('dataBW15.csv', newline='') as csvfile:
    dataBW15 = list(csv.reader(csvfile))

with open('dataCW17.csv', newline='') as csvfile:
    dataCW17 = list(csv.reader(csvfile))

with open('dataDW17.csv', newline='') as csvfile:
    dataDW17 = list(csv.reader(csvfile))

with open('dataE.csv', newline='') as csvfile:
    dataE = list(csv.reader(csvfile))

# convert data to float
dataAW10 = [[float(x) for x in row] for row in dataAW10]
dataAW11 = [[float(x) for x in row] for row in dataAW11]
dataBW1 = [[float(x) for x in row] for row in dataBW1]
dataBW3 = [[float(x) for x in row] for row in dataBW3]
dataBW15 = [[float(x) for x in row] for row in dataBW15]
dataCW17 = [[float(x) for x in row] for row in dataCW17]
dataDW17 = [[float(x) for x in row] for row in dataDW17]
dataE = [[float(x) for x in row] for row in dataE]


# define function
def wheat(data):
    r_2 = [ufloat(data[i][0], data[i][0] * 0.002) for i in range(0, 3)]
    r_3 = [data[i][1] for i in range(0, 3)]
    r_4 = [data[i][2] for i in range(0, 3)]
    r_ratio = [ufloat(r_3[i] / r_4[i], (r_3[i] / r_4[i]) * 0.005) for i in range(0, 3)]
    r_x = [r_2[i] * r_ratio[i] for i in range(0, 3)]
    return np.mean(r_x)


latex('R_{10}', wheat(dataAW10).n, wheat(dataAW10).s, '\ohm', 0, 2)
R_10 = wheat(dataAW10)
latex('R_{11}', wheat(dataAW11).n, wheat(dataAW11).s, '\ohm', 0, 2)
R_11 = wheat(dataAW11)


def kapa1(data):
    c_2 = [ufloat(data[i][0], data[i][0] * 0.002) for i in range(0, 2)]
    r_3 = [data[i][2] for i in range(0, 2)]
    r_4 = [data[i][3] for i in range(0, 2)]
    r_ratio = [ufloat(r_4[i] / r_3[i], (r_4[i] / r_3[i]) * 0.005) for i in range(0, 2)]
    c_x = [c_2[i] * r_ratio[i] for i in range(0, 2)]
    return np.mean(c_x)


def kapa2(data):
    r_2 = [ufloat(data[i][1], data[i][1] * 0.03) for i in range(0, 2)]
    r_3 = [data[i][2] for i in range(0, 2)]
    r_4 = [data[i][3] for i in range(0, 2)]
    r_ratio = [ufloat(r_3[i] / r_4[i], (r_3[i] / r_4[i]) * 0.005) for i in range(0, 2)]
    r_x = [r_2[i] * r_ratio[i] for i in range(0, 2)]
    return np.mean(r_x)


latex('C_{15}', kapa1(dataBW15).n, kapa1(dataBW15).s, '\ nano\F', 0, 2)
C_15 = kapa1(dataBW15)
latex('R_{15}', kapa2(dataBW15).n, kapa2(dataBW15).s, '\ohm', 0, 2)
R_15 = kapa2(dataBW15)

latex('C_{1}', kapa1(dataBW1).n, kapa1(dataBW1).s, '\ nano\F', 0, 2)
C_1 = kapa1(dataBW1)
latex('C_{3}', kapa1(dataBW3).n, kapa1(dataBW3).s, '\ nano\F', 0, 2)
C_3 = kapa1(dataBW3)


def indu(data):
    l_2 = [ufloat(data[i][0], data[i][0] * 0.002) for i in range(0, 3)]
    r_3 = [data[i][2] for i in range(0, 3)]
    r_4 = [data[i][3] for i in range(0, 3)]
    r_ratio = [ufloat(r_3[i] / r_4[i], (r_3[i] / r_4[i]) * 0.005) for i in range(0, 3)]
    l_x = [l_2[i] * r_ratio[i] for i in range(0, 3)]
    return np.mean(l_x)


latex('L_{17}', indu(dataCW17).n, indu(dataCW17).s, '\milli\H', 0, 2)
L_17i = indu(dataCW17)
latex('R_{17}', kapa2(dataCW17).n, kapa2(dataCW17).s, '\ohm', 0, 2)
R_17i = kapa2(dataCW17)


def max1(data):
    r_2 = [ufloat(data[i][1], data[i][1] * 0.002) for i in range(0, 3)]
    r_3 = [data[i][2] for i in range(0, 3)]
    r_4 = [data[i][3] for i in range(0, 3)]
    r_ratio = [ufloat(r_3[i] / r_4[i], (r_3[i] / r_4[i]) * 0.005) for i in range(0, 3)]
    r_x = [r_2[i] * r_ratio[i] for i in range(0, 3)]
    return np.mean(r_x)


def max2(data):
    c_2 = [ufloat(data[i][0] * 10 ** -9, data[i][0] * 10 ** -9 * 0.002) for i in range(0, 3)]
    r_2 = [ufloat(data[i][1], data[i][1] * 0.002) for i in range(0, 3)]
    r_3 = [ufloat(data[i][2], data[i][2] * 0.03) for i in range(0, 3)]
    l_x = [c_2[i] * r_2[i] * r_3[i] for i in range(0, 3)]
    return np.mean(l_x)


latex('Max R_{17}', max1(dataDW17).n, max1(dataDW17).s, '\ohm', 0, 2)
R_17m = max1(dataDW17)
latex('Max L_{17}', max2(dataDW17).n * 1000, max2(dataDW17).s * 1000, '\milli\H', 0, 2)
L_17m = max2(dataDW17) * 1000

R = 1000
C = 660 * 10 ** -9
w_0 = 1 / (2 * np.pi * R * C)
#
for i in range(0, 32):
    dataE[i][1] = dataE[i][1] / 2.3
    dataE[i][0] = dataE[i][0] / w_0


def wienRobinson(x):
    return np.sqrt(1 / 9 * ((x ** 2 - 1) ** 2) / ((1 - x ** 2) ** 2 + 9 * x ** 2))

x = [dataE[i][0] for i in range(0, 32)]
p= (np.linspace(x[0],x[-1],10000))

plt.plot([np.log(x[0]) for x in dataE], [x[1] for x in dataE], 'o', label=r'Messdaten')
plt.plot(np.log(p), wienRobinson(p), label=r'Theoriekurve')
plt.legend(loc='lower right')
plt.xlabel(r'$\ln(\frac{\omega}{\omega_0})$')
plt.ylabel(r'$\frac{U_{br}}{U_{s}}$')
plt.savefig('plotE.pdf')
print(dataE)

LR_10 = 239
LR_11 = 489.9
LC_15 = 652
LR_15 = 473
LC_1 = 660
LC_3 = 420
LR_17i = 93.65
LL_17i = 41.85
LR_17m = 93.65
LL_17m = 41.85

AR_10 = abs(((R_10 - LR_10)/LR_10)*100)
AR_11 = abs(((R_11 - LR_11)/LR_11)*100)
AC_15 = abs(((C_15 - LC_15)/LC_15)*100)
AR_15 = abs(((R_15 - LR_15)/LR_15)*100)
AC_1 = abs(((C_1 - LC_1)/LC_1)*100)
AC_3 = abs(((C_3 - LC_3)/LC_3)*100)
AR_17i = abs(((R_17i - LR_17i)/LR_17i)*100)
AL_17i = abs(((L_17i - LL_17i)/LL_17i)*100)
AR_17m = abs(((R_17m - LR_17m)/LR_17m)*100)
AL_17m = abs(((L_17m - LL_17m)/LL_17m)*100)

print(R_17m)
print(LR_17m)

latex('AR_{10}', AR_10.n, AR_10.s, '\%', 0, 2)
latex('AR_{11}', AR_11.n, AR_11.s, '\%', 0, 2)
latex('AC_{15}', AC_15.n, AC_15.s, '\%', 0, 2)
latex('AR_{15}', AR_15.n, AR_15.s, '\%', 0, 2)
latex('AC_{1}', AC_1.n, AC_1.s, '\%', 0, 2)
latex('AC_{3}', AC_3.n, AC_3.s, '\%', 0, 2)
latex('AR_{17i}', AR_17i.n, AR_17i.s, '\%', 0, 2)
latex('AL_{17i}', AL_17i.n, AL_17i.s, '\%', 0, 2)
latex('AR_{17m}', AR_17m.n, AR_17m.s, '\%', 0, 2)
latex('AL_{17m}', AL_17m.n, AL_17m.s, '\%', 0, 2)