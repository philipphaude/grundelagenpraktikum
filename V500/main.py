import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from uncertainties import ufloat


# def for latex output
def latex(w_name, w, w_err, w_unit, magnitude, digits):
    print(w_name, '&=', '\SI{', round(w / (10 ** magnitude), digits), '(', round(w_err / (10 ** magnitude), digits),
          ')e', magnitude, '}{', w_unit, '}')


# set up la matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx} \sisetup{per-mode=fraction, exponent-product = \cdot, '
                              r'separate-uncertainty = true, output-decimal-marker = {,}}')

# read from csv file
with open('dataGreen.csv', newline='') as csvfile:
    dataGreen = list(csv.reader(csvfile))

with open('dataRed.csv', newline='') as csvfile:
    dataRed = list(csv.reader(csvfile))

with open('dataYellow.csv', newline='') as csvfile:
    dataYellow = list(csv.reader(csvfile))

with open('dataViolet.csv', newline='') as csvfile:
    dataViolet = list(csv.reader(csvfile))

with open('dataYellowAll.csv', newline='') as csvfile:
    dataYellowAll = list(csv.reader(csvfile))

# convert data to float
dataGreen = [[float(x) for x in row] for row in dataGreen]
dataRed = [[float(x) for x in row] for row in dataRed]
dataYellow = [[float(x) for x in row] for row in dataYellow]
dataViolet = [[float(x) for x in row] for row in dataViolet]
dataYellowAll = [[float(x) for x in row] for row in dataYellowAll]

# plot dataYellowAll
plt.plot([x[0] for x in dataYellowAll], [x[1] for x in dataYellowAll], 'x', label='Messdaten', color='orange')

# format and save plot
plt.xlabel(r'$U$ / V')
plt.ylabel(r'$I$ / $\SI{}{\nano\A}$')
plt.legend(loc = 'upper left')
plt.savefig('plots/dataYellowAll.pdf')

plt.clf()

# plot dataYellow
plt.plot([x[0] for x in dataYellow], [(x[1] ** 0.5) for x in dataYellow], 'x', label='Messdaten', color='orange')

# do a linear regression on dataYellow with scipy
slope, intercept, r_value, p_value, std_err = sp.stats.linregress([row[0] for row in dataYellow[:5]],
                                                                  [(row[1] ** 0.5) for row in dataYellow[:5]])
result = sp.stats.linregress([row[0] for row in dataYellow[:5]], [(row[1] ** 0.5) for row in dataYellow[:5]])
xx = np.linspace(-0.7, 2.1, 100)
plt.plot(xx, intercept + slope * xx, color='purple', label=r'lineare Regression')

# format and save plot
plt.xlabel(r'$U$ / V')
plt.ylabel(r'$\sqrt{I}$ / $\sqrt{\SI{}{\nano\A}}$')
plt.xlim(-0.7, 2.2)
plt.ylim(-0.25, 2)
plt.legend(loc='upper left')
plt.savefig('plots/dataYellow.pdf')

# output slope and intercept
latex('m Yellow', slope, std_err, '\V\s', 0, 3)
latex('n Yellow', intercept, result.intercept_stderr, '\V\s', 0, 3)

# declare slope and intercept as uncertainties
m = ufloat(slope, std_err)
n = ufloat(intercept, result.intercept_stderr)
U_Yellow = ufloat(0, 0)

# calculate y=0 from mx+n
U_Yellow = - (n / m)

# output x
latex('U_g Yellow', U_Yellow.n, U_Yellow.s, '\V\s', 0, 3)

plt.clf()

# plot dataGreen
plt.plot([x[0] for x in dataGreen], [(x[1] ** 0.5) for x in dataGreen], 'x', label='Messdaten', color='green')

# do a linear regression on dataGreen with scipy
slope, intercept, r_value, p_value, std_err = sp.stats.linregress([row[0] for row in dataGreen[:8]],
                                                                  [(row[1] ** 0.5) for row in dataGreen[:8]])
result = sp.stats.linregress([row[0] for row in dataGreen[:8]], [(row[1] ** 0.5) for row in dataGreen[:8]])
xx = np.linspace(-0.7, 2.1, 100)
plt.plot(xx, intercept + slope * xx, color='red', label=r'lineare Regression')

# format and save plot
plt.xlabel(r'$U$ / V')
plt.ylabel(r'$\sqrt{I}$ / $\sqrt{\SI{}{\nano\A}}$')
plt.xlim(-0.7, 2.1)
plt.ylim(-0.5, 3)
plt.legend(loc='upper left')
plt.savefig('plots/dataGreen.pdf')

# output slope and intercept
latex('m Green', slope, std_err, '\V\s', 0, 3)
latex('n Green', intercept, result.intercept_stderr, '\V\s', 0, 3)

# declare slope and intercept as uncertainties
m = ufloat(slope, std_err)
n = ufloat(intercept, result.intercept_stderr)
U_Green = ufloat(0, 0)

# calculate y=0 from mx+n
U_Green = - (n / m)

# output x
latex('U_g Green', U_Green.n, U_Green.s, '\V\s', 0, 3)

plt.clf()

# plot dataRed in red
plt.plot([x[0] for x in dataRed], [(x[1] ** 0.5) for x in dataRed], 'x', label='Messdaten', color='red')

# do a linear regression on dataRed with scipy
slope, intercept, r_value, p_value, std_err = sp.stats.linregress([row[0] for row in dataRed[:5]],
                                                                  [(row[1] ** 0.5) for row in dataRed[:5]])
result = sp.stats.linregress([row[0] for row in dataRed[:5]], [(row[1] ** 0.5) for row in dataRed[:5]])
xx = np.linspace(-1.2, 2.1, 100)
plt.plot(xx, intercept + slope * xx, color='green', label=r'lineare Regression')

# format and save plot
plt.xlabel(r'$U$ / V')
plt.ylabel(r'$\sqrt{I}$ / $\sqrt{\SI{}{\nano\A}}$')
plt.xlim(-1.2, 2.1)
plt.ylim(-0.05, 0.3)
plt.legend(loc='upper left')
plt.savefig('plots/dataRed.pdf')

# output slope and intercept
latex('m Red', slope, std_err, '\V\s', 0, 3)
latex('n Red', intercept, result.intercept_stderr, '\V\s', 0, 3)

# declare slope and intercept as uncertainties
m = ufloat(slope, std_err)
n = ufloat(intercept, result.intercept_stderr)
U_Red = ufloat(0, 0)

# calculate y=0 from mx+n
U_Red = - (n / m)

# output x
latex('U_g Red', U_Red.n, U_Red.s, '\V\s', 0, 3)

plt.clf()

# plot dataViolet in violet
plt.plot([x[0] for x in dataViolet], [(x[1] ** 0.5) for x in dataViolet], 'x', label='Messdaten', color='purple')

# do a linear regression on dataViolet with scipy
slope, intercept, r_value, p_value, std_err = sp.stats.linregress([row[0] for row in dataViolet[:11]],
                                                                  [(row[1] ** 0.5) for row in dataViolet[:11]])
result = sp.stats.linregress([row[0] for row in dataViolet[:11]], [(row[1] ** 0.5) for row in dataViolet[:11]])
xx = np.linspace(-1.5, 2.3, 100)
plt.plot(xx, intercept + slope * xx, color='orange', label=r'lineare Regression')

# format and save plot
plt.xlabel(r'$U$ / V')
plt.ylabel(r'$\sqrt{I}$ / $\sqrt{\SI{}{\nano\A}}$')
plt.xlim(-1.5, 2.3)
plt.ylim(-0.5, 3)
plt.legend(loc='upper left')
plt.savefig('plots/dataViolet.pdf')

# output slope and intercept
latex('m Violet', slope, std_err, '\V\s', 0, 3)
latex('n Violet', intercept, result.intercept_stderr, '\V', 0, 3)

# declare slope and intercept as uncertainties
m = ufloat(slope, std_err)
n = ufloat(intercept, result.intercept_stderr)
U_Violet = ufloat(0, 0)

# calculate y=0 from mx+n
U_Violet = - (n / m)

# output x
latex('U_g Violett', U_Violet.n, U_Violet.s, '\V\s', 0, 3)

plt.clf()

# define frequencies
f_Yellow = sp.constants.c / (579.1 * 10 ** (-9))
f_Green = sp.constants.c / (546.1 * 10 ** (-9))
f_Red = sp.constants.c / (623.4 * 10 ** (-9))
f_Violet = sp.constants.c / (435.8 * 10 ** (-9))

# print frequencies in THz
print('f Yellow: ', f_Yellow * 10 ** (-12), 'THz')
print('f Green: ', f_Green * 10 ** (-12), 'THz')
print('f Red: ', f_Red * 10 ** (-12), 'THz')
print('f Violet: ', f_Violet * 10 ** (-12), 'THz')

# plot frequencies against U_g
plt.plot([f_Yellow, f_Green, f_Red, f_Violet], [-U_Yellow.n, -U_Green.n, -U_Red.n, -U_Violet.n], 'x', label='Messdaten',
         color='black')

# do a linear regression on frequencies and U_g
slope, intercept, r_value, p_value, std_err = sp.stats.linregress([f_Yellow, f_Green, f_Red, f_Violet],
                                                                  [-U_Yellow.n, -U_Green.n, -U_Red.n, -U_Violet.n])
result = sp.stats.linregress([f_Yellow, f_Green, f_Red, f_Violet], [-U_Yellow.n, -U_Green.n, -U_Red.n, -U_Violet.n])
xx = np.linspace(450 * 10 ** 12, 700 * 10 ** 12, 100)
plt.plot(xx, intercept + slope * xx, color='black', label=r'lineare Regression')

# output slope and intercept
latex('m Freq', slope, std_err, r'\tera\Hz', -15, 3)
latex('n Freq', intercept, result.intercept_stderr, '\V', 0, 3)

#format plot
plt.xlabel(r'$f$ / THz')
plt.ylabel(r'$U_g$ / V')
plt.xlim(450 * 10**12, 700 * 10**12)
plt.ylim(0.2, 1.2)
plt.legend(loc = 'upper left')

#change xticks to 10**12
plt.xticks([450 * 10**12, 500 * 10**12, 550 * 10**12, 600 * 10**12, 650 * 10**12, 700 * 10**12], ['450', '500', '550', '600', '650', '700'])

#save plot
plt.savefig('plots/frequencies.pdf')

h = sp.constants.h/sp.constants.e
print(std_err)
p = ufloat(slope, std_err) / h
print('p: ', p.n , p.s)

plt.clf()

#plot frequencies against U_g without red data point
plt.plot([f_Yellow, f_Green, f_Violet], [-U_Yellow.n, -U_Green.n, -U_Violet.n], 'x', label='Messdaten', color ='black')

#do a linear regression on frequencies and U_g withot the red data point
slope, intercept, r_value, p_value, std_err = sp.stats.linregress([f_Yellow, f_Green, f_Violet], [-U_Yellow.n, -U_Green.n,  -U_Violet.n])
result = sp.stats.linregress([f_Yellow, f_Green, f_Violet], [-U_Yellow.n, -U_Green.n, -U_Violet.n])
xx = np.linspace(450 * 10**12, 700 * 10**12, 100)
plt.plot(xx, intercept + slope * xx, color='black', label=r'lineare Regression')

#output slope and intercept
latex('m Freq without Red', slope, std_err, r'\tera\Hz', -15, 3)
latex('n Freq without Red', intercept, result.intercept_stderr, '\V', 0, 3)

#format plot
plt.xlabel(r'$f$ / THz')
plt.ylabel(r'$U_g$ / V')
plt.xlim(450 * 10**12, 700 * 10**12)
plt.ylim(0.2, 1.2)
plt.legend(loc = 'upper left')

#change xticks to 10**12
plt.xticks([450 * 10**12, 500 * 10**12, 550 * 10**12, 600 * 10**12, 650 * 10**12, 700 * 10**12], ['450', '500', '550', '600', '650', '700'])

#save plot
plt.savefig('plots/frequenciesWithoutRed.pdf')

h = sp.constants.h/sp.constants.e
print(std_err)
p_without_red = ufloat(slope, std_err) / h
print('p_without_red: ', p_without_red)