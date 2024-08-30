import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.ticker import FixedLocator, FixedFormatter

# x axis transformation
xPositiveScale = 10
def forward(x):
    # Apply different scaling based on x-values
    return np.piecewise(x, [x < 0, x >= 0], [lambda x: x, lambda x: x*xPositiveScale])

def inverse(x):
    # Apply the inverse scaling functions to match the forward transformation
    return np.piecewise(x, [x < 0, x >= 0], [lambda x: x, lambda x: x/xPositiveScale])

def plot_diode_data(inFile, outFile, title):
    data = np.genfromtxt(inFile, delimiter=',', skip_header=1)
    U = data[:, 0]
    I = data[:, 1]
    U_err = data[:, 2]
    I_err = data[:, 3]

    fig, ax = plt.subplots()

    ax.errorbar(U, I, I_err, U_err, color='xkcd:blue')

    ax.set_xlabel(r'$U/$V')
    ax.set_ylabel(r'$I/$mA')
    ax.set_title(title)
    ax.grid(True, which='major')

    # Set the custom transform for the y-axis
    ax.set_xscale('function', functions=(forward, inverse))

    ticks = np.concatenate((
        np.arange(-15, 0, 2.5), np.arange(0, 2, 0.2)
    ))
    minorTicks = np.concatenate((
        np.arange(-15, 0, 0.5), np.arange(0, 2, 0.1)
    ))
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_minor_locator(FixedLocator(minorTicks))

    fig.savefig(outFile)
    # TODO: different scaling below and above zero

plot_diode_data('ep2/data/1_D1.csv', 'ep2/plot/1_D1.pdf', 'Kennlinie D1')
plot_diode_data('ep2/data/1_D2.csv', 'ep2/plot/1_D2.pdf', 'Kennlinie D2')