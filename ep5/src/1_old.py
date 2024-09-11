import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def get_data_pd(filename):
    return pd.read_csv(filename, sep=',', skipinitialspace=True)

def setup_plot(fig, ax):
    """     xPositiveScale = 10
    def transform_forward(y):
        # Apply different scaling based on x-values
        return 20*np.log(y)

    def transform_inverse(y):
        # Apply the inverse scaling functions to match the forward transformation
        return np.exp(y/20)

    ax.set_yscale('function', functions=(transform_forward, transform_inverse)) """

    ax.set_xscale('log')
    ax.set_yscale('log')


def plot_data(fig, ax, data, plotFile):
    data = data
    ax.plot(2, 2)
    fig.savefig(plotFile)


fig, ax = plt.subplots()
setup_plot(fig, ax)

data = get_data_pd('ep5/data/1a.csv')
plot_data(fig, ax, data, 'ep5/plot/1.pdf')

