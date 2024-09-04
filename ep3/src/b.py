import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_data_pd(filename):
    return pd.read_csv(filename, sep=',', skipinitialspace=True)

def process_data(data, dataFile, plotFile):
    # data processing
    U_Derr = 0.1
    dU_GS = 0.2412
    dU_GSerr = 0.0012

    n = data['n']
    U_D = data['U_D/V']

    I_D = U_D / 500
    I_Derr = U_Derr / 500
    Up = n * dU_GS # U'
    Up_err = n * dU_GSerr
    U_GS = Up - 100 * I_D
    U_GSerr = np.sqrt(Up_err**2 + (100 * I_Derr)**2)
    I_Dsqrt = np.sqrt(I_D)
    I_DsqrtErr = .5 * I_Derr / np.sqrt(I_D)

    I_D *= 1000; I_Derr *=1000
    data['I_D/mA'] = I_D
    # data['I_Derr/mA'] = I_Derr
    data["U'/V"] = Up
    data['U_GS'] = U_GS
    data['I_Dsqrt'] = I_Dsqrt
    data['I_DsqrtErr'] = I_DsqrtErr

    data.to_csv(dataFile, index=False)

    # plotting
    fig, ax = plt.subplots()
    ax.errorbar(U_GS, I_D, I_Derr, U_GSerr, ls='None', label='Messdaten', color='xkcd:blue')

    def quadratic_fit(U_GS, k, U_thr):
        return k * (U_GS - U_thr)**2
    # TODO: chisq fit

    ax.set_xlabel(r'$U_{GS}/V$')
    ax.set_ylabel(r'$I_{D}/mA$')

    fig.savefig(plotFile)


data = get_data_pd('ep3/data/b_raw.csv')
process_data(data, 'ep3/data/b.csv', 'ep3/plot/b.pdf')