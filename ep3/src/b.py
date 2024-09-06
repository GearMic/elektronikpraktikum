import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimize

def data_range(data, overhang=0, nPoints=100):
    min, max = np.min(data), np.max(data)
    span = max-min

    return np.linspace(min-overhang*span, max+overhang*span, nPoints)


def get_data_pd(filename):
    return pd.read_csv(filename, sep=',', skipinitialspace=True)

def process_data(data, dataFile, plotFile1, plotFile2):
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

    print('Errors: I_D:', I_Derr)

    I_D *= 1000; I_Derr *=1000
    I_Dsqrt = np.sqrt(I_D)
    I_DsqrtErr = .5 * I_Derr / np.sqrt(I_D)
    data['I_D/mA'] = I_D
    # data['I_Derr/mA'] = I_Derr
    data["U'/V"] = Up
    data["U'err"] = Up_err
    data['U_GS'] = U_GS
    data['U_GSerr'] = U_GSerr
    data['I_Dsqrt'] = I_Dsqrt
    data['I_DsqrtErr'] = I_DsqrtErr


    # plot 2
    fig, ax = plt.subplots()
    ax.errorbar(U_GS, I_Dsqrt, I_DsqrtErr, U_GSerr, ls='None', label='Messdaten', color='xkcd:blue')

    ax.set_xlabel(r'$U_{GS}/V$')
    ax.set_ylabel(r'$\sqrt{I_D}/\sqrt{mA}$')
    ax.legend()
    ax.minorticks_on()
    ax.grid(True, which='both')

    fig.savefig(plotFile2)

    # plot 1 (with fit)
    fig, ax = plt.subplots()
    ax.errorbar(U_GS, I_D, I_Derr, U_GSerr, ls='None', label='Messdaten', color='xkcd:blue', zorder=10)

    # def quadratic(B, x):
    #     k, U_thr = B
    #     return k * (U_GS - U_thr)**2
    # data = RealData(U_GS, I_D, sx=U_GSerr, sy=I_Derr)
    # # Create a Model object for the quadratic function
    # quadratic_model = Model(quadratic_fit)
    # # Set up the ODR with the model and data
    # odr = ODR(data, quadratic_model, beta0=[1, 1])
    # # Run the ODR fit
    # output = odr.run()

    # fitting
    def quadratic(U_GS, k, U_thr):
        return k * (U_GS - U_thr)**2
    
    popt, pcov = optimize.curve_fit(quadratic, U_GS, I_D, p0=(1, 1), sigma=I_Derr)
    k, U_thr = popt
    kErr, U_thrErr = np.sqrt(np.diag(pcov))
    print('k =', k, kErr)
    print('U_thr =', U_thr, U_thrErr)

    xFit = data_range(U_GS, 0.1)
    yFit = quadratic(xFit, k, U_thr)
    ax.plot(xFit, yFit, label=r'quadratischer $\chi^2$-Fit', color='xkcd:red')

    ax.set_xlabel(r'$U_{GS}/V$')
    ax.set_ylabel(r'$I_{D}/mA$')
    ax.minorticks_on()
    ax.grid(True, which='both')
    ax.legend()

    fig.savefig(plotFile1)

    # export data
    dataExport = data.copy()
    # dataExport['n'] = dataExport['n'].map(lambda x: f"{x}")
    dataExport['I_Dsqrt'] = dataExport['I_Dsqrt'].map(lambda x: f"{x:.3f}")
    dataExport['I_DsqrtErr'] = dataExport['I_DsqrtErr'].map(lambda x: f"{x:.3f}")
    dataExport.to_csv(dataFile, index=False, float_format='%.2f')

    return data, (k, U_thr, kErr, U_thrErr, I_Derr)


def calc_gm(dataIn, params, dataFile):
    k, U_thr, kErr, U_thrErr, I_Derr = params

    U_GS = dataIn['U_GS']
    I_D = dataIn['I_D/mA']
    # I_Derr = dataIn['I_Derr/mA']

    g_m1 = 2*k*(U_GS-U_thr)
    g_m1Err = 2*kErr*(U_GS-U_thr) # works for kErr >> U_GSerr or U_thrErr

    g_m2 = 2*np.sqrt(k*I_D)
    # g_m2Err = 2*np.sqrt((kErr**2 + I_Derr**2) / (k*I_D))
    g_m2Err = 2*np.sqrt(kErr**2 * I_D / k + I_Derr**2 * k / I_D)

    data = pd.DataFrame({
        'U_GS': U_GS, 'I_D/mA': I_D,
        'g_m1': g_m1, 'g_m1Err': g_m1Err, 'g_m2': g_m2, 'g_m2Err': g_m2Err
    })
    data.to_csv(dataFile, index=False, float_format='%.2f')

    

data = get_data_pd('ep3/data/b_raw.csv')
data, params = process_data(data, 'ep3/data/b_processed.csv', 'ep3/plot/b1.pdf', 'ep3/plot/b2.pdf')
calc_gm(data, params, 'ep3/data/b_gm.csv')