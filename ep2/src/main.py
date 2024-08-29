import numpy as np
import matplotlib.pyplot as plt

def plot_diode_data(inFile, outFile):
    data = np.genfromtxt(inFile, delimiter=',')
    U = data[:, 0]
    I = data[:, 1]
    U_err = data[:, 2]
    I_err = data[:, 3]

    fig, ax = plt.subplots()

    ax.errorbar(U, I, I_err, U_err, color='xkcd:blue')

    ax.set_xlabel(r'$U/$V')
    ax.set_ylabel(r'$I/$mA')
    ax.minorticks_on()
    ax.grid(True, which='both')

    fig.savefig(outFile)
    # TODO: different scaling below and above zero

plot_diode_data('ep2/data/1_D1.csv', 'ep2/plot/1_D1.pdf')
# plot_diode_data('ep2/data/1_d1.csv', 'ep2/plot/1_D1.pdf')