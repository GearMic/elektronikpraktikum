import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('ep0/data/c.csv', delimiter=',')
print(data)

nu = data[:, 0]
U = 20 * np.log10(data[:, 1]/20)

fig, ax = plt.subplots()

ax.plot(nu, U, '.', color='xkcd:blue', label='Messwerte')
ax.axhline(-3, color='xkcd:orange', label=r'-3$\mathrm{dB}$-Linie')
ax.plot((3650), (-3), 'x', color='xkcd:orange', label=r'Schnittpunkt mit -3$\mathrm{dB}$-Linie')

ax.set_xscale('log')
ax.xaxis.set_major_formatter(plt.ScalarFormatter())

# ax.set_title('Bode-Diagramm RC-Tiefpass')
ax.set_xlabel(r'$f/\mathrm{Hz}$')
# plt.ylabel(r'$U/{\mathrm{V}_\mathrm{pp}}$')
ax.set_ylabel(r'$20 \log(U/20\mathrm{V})$')
ax.minorticks_on()
# ax.grid('both')
ax.grid(True, which='both')#, linestyle=':', linewidth='0.5', color='gray')
ax.legend()

fig.savefig('ep0/plot/c.pdf')