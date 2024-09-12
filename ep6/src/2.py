import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pandas as pd

def get_data_pd(filename):
    return pd.read_csv(filename, sep=',', skipinitialspace=True)

def plot_data(data, plotFile):
    f = np.array(data['f/kHz'])
    v = np.array(data['v'])
    v_err = np.array(data['v_err'])

    fig, ax = plt.subplots()
    ax.set_xscale('log')
    ax.xaxis.set_major_formatter(ScalarFormatter())

    ax.errorbar(f, v, v_err, color='xkcd:blue', linestyle="None", elinewidth=1.0, marker="x")

    ax.set_xlabel(r'$f/\mathrm{kHz}$')
    ax.set_ylabel(r'$|v|$')
    ax.grid(True, which='both')
    plt.tight_layout()
    fig.savefig(plotFile)
    

data = get_data_pd('../data/2.csv')
plot_data(data, '../plot/2.pdf')

