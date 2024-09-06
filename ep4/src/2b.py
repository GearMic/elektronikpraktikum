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

def format_df_column(df, index, formatString):
    df[index] = df[index].map(lambda x: formatString.format(x))

def process_data(data, dataFile):
    # data.columns = data.columns.str.strip()

    U_C = np.array(data["U_C/V_SS"])
    U_B = np.array(data["U_B/V_SS"])
    dU = np.array(data["dU/V"])
    R_C = np.array(data["R_C/ohm"])
    R_E = np.array(data["R_E/ohm"])

    # v = np.round(U_C/U_B,2)
    # dv = np.round(np.sqrt((dU/U_B)*(dU/U_B)+((U_C*dU)/(U_B*U_B))*((U_C*dU)/(U_B*U_B))),2)
    v_exp = U_C/U_B
    dv_exp = np.sqrt((dU/U_B)*(dU/U_B)+((U_C*dU)/(U_B*U_B))*((U_C*dU)/(U_B*U_B)))
    v_theo = R_C/R_E
    v_rec = 1/v_exp # reciprocal of v
    dv_rec = dv_exp / v_exp**2

    dataAdd = pd.DataFrame()
    dataAdd["v_theo"]=v_theo
    dataAdd["v_exp"]=v_exp
    dataAdd["dv_exp"]=dv_exp
    dataAdd["v_rec"]=v_rec
    dataAdd["dv_rec"]=dv_rec
    # data["dv_theo"]=dv_theo

    data = pd.concat((data, dataAdd), axis=1)
    # data['v_theo'] = 
    format_df_column(data, 'v_theo', '{:.2f}')
    format_df_column(data, 'v_exp', '{:.2f}')
    format_df_column(data, 'dv_exp', '{:.2f}')

    data.to_csv(dataFile, index=False, float_format='%.3f')
    return data

def plot_vrec_of_RE(data, plotFile):
    R_C = np.array(data["R_C/ohm"])
    mask = R_C==390

    R_E = np.array(data["R_E/ohm"])[mask]
    v_rec = -np.array(data["v_rec"])[mask]
    dv_rec = np.array(data["dv_rec"])[mask]

    # plot
    fig, ax = plt.subplots()
    ax.errorbar(R_E, v_rec, dv_rec, fmt='x', ls='none', label=r'Messdaten ($R_C=390\mathrm{\Omega}$)', color='xkcd:blue', zorder=10)

    ax.set_xlabel(r'$R_E/\mathrm{\Omega}$')
    ax.set_ylabel(r'$\frac{1}{v}$')
    ax.minorticks_on()
    ax.grid(True, which='both')

    # fit
    # def fit_fn(R_E, v_0, R_Cfit):
    #     return 1/v_0 - R_E/R_Cfit 

    # popt, pcov = optimize.curve_fit(fit_fn, R_E, v_rec, p0=(10000, 390), sigma=dv_rec)
    # v_0, R_Cfit = popt
    # v_0err, R_CfitErr = np.sqrt(np.diag(pcov))
    # print('R_E, R_Cfit', v_0, v_0err, ',', R_Cfit, R_CfitErr)

    def fit_fn(R_E, v_0):
        return 1/v_0 - R_E/390 

    R_E = R_E[:-2]
    v_rec = v_rec[:-2]
    dv_rec = dv_rec[:-2]

    popt, pcov = optimize.curve_fit(fit_fn, R_E, v_rec, p0=(-10), sigma=dv_rec)
    v_0 = popt
    v_0err = np.sqrt(pcov)
    # print('R_E, R_Cfit', v_0, v_0err, ',', R_Cfit, R_CfitErr)
    print('v_0', v_0, v_0err)

    xFit = data_range(R_E, 0.05)
    yFit = fit_fn(xFit, v_0)#, R_Cfit)
    ax.plot(xFit, yFit, label=r'$\chi^2$-Fit', color='xkcd:red')
    ax.legend()

    fig.savefig(plotFile)


def plot_v_of_RC(data, plotFile):
    R_E = np.array(data["R_E/ohm"])
    mask = R_E==390

    R_C = np.array(data["R_C/ohm"])[mask]
    v_exp = -np.array(data["v_exp"], dtype=float)[mask]
    dv_exp = np.array(data["dv_exp"], dtype=float)[mask]

    # plot
    fig, ax = plt.subplots()
    ax.errorbar(R_C, v_exp, dv_exp, fmt='x', ls='none', label=r'Messdaten ($R_E=390\mathrm{\Omega}$)', color='xkcd:blue', zorder=10)

    ax.set_xlabel(r'$R_C/\mathrm{\Omega}$')
    ax.set_ylabel(r'$v$')
    ax.legend(loc='upper left')
    ax.minorticks_on()
    ax.grid(True, which='both')
    
    # fit
    def fit_fn(R_C, zeta):
        return -zeta * R_C

    popt, pcov = optimize.curve_fit(fit_fn, R_C, v_exp, p0=(-10), sigma=dv_exp)
    zeta = popt
    zetaErr = np.sqrt(pcov)
    print('zeta', zeta, zetaErr)

    xFit = data_range(R_C, 0.05)
    yFit = fit_fn(xFit, zeta)#, R_Cfit)
    ax.plot(xFit, yFit, label=r'$\chi^2$-Fit', color='xkcd:red')
    ax.legend()

    fig.savefig(plotFile)

    fig.savefig(plotFile)




data = get_data_pd('ep4/data/2b.csv')
data = process_data(data, 'ep4/data/2b_out.csv')
plot_vrec_of_RE(data, 'ep4/plot/2c1.pdf')
plot_v_of_RC(data, 'ep4/plot/2c2.pdf')