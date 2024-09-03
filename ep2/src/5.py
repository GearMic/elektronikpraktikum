import numpy as np
import matplotlib.pyplot as plt

def load_data(filename):
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)
    return data

def plot_data(fig, ax, data, label, color):
    U, I, Uerr, Ierr = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    ax.errorbar(I, U, Uerr, Ierr, label=label, color=color, linestyle='none')

# I, U, Ierr, Uerr = load_data('ep2/data/5a.csv')

fig, ax = plt.subplots()
plot_data(fig, ax, load_data('ep2/data/5a.csv'), 'ohne Zenerdiode', 'xkcd:blue')
plot_data(fig, ax, load_data('ep2/data/5b.csv'), 'mit Zenerdiode', 'xkcd:red')

ax.grid()
ax.set_xlabel('$I$/mA')
ax.set_ylabel('$U$/V')
ax.legend()

fig.savefig('ep2/plot/5.pdf')