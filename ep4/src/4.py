import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_data_pd(filename):
    return pd.read_csv(filename, sep=',', skipinitialspace=True)

def process_data(data, dataFile):
    data.columns = data.columns.str.strip()

    U_C = np.array(data["U_C/Vpp"])
    U_B = np.array(data["U_B/Vpp"])
    dU = np.array(data["dU/V"])

    v = np.round(U_C/U_B,2)
    dv = np.round(np.sqrt((dU/U_B)*(dU/U_B)+((U_C*dU)/(U_B*U_B))*((U_C*dU)/(U_B*U_B))),2)

    data["v"]=v
    data["dv"]=dv

    data.to_csv(dataFile, index=False)
    return data

def plot_data(data1, data2):

    ### Messwerte plotten:
    x_data1 = np.log10(1000 * data1["f/kHz"])
    y_data1 = 20 * np.log10(data1["v"])
    x_data2 = np.log10(1000 * data2["f/kHz"])
    y_data2 = 20 * np.log10(data2["v"])

    color_transistor = "r"
    color_kaskode = "b"
    line_transistor = 16.8
    line_kaskode = 16.94

    fig, ax = plt.subplots()
    ax.scatter(x_data1,y_data1,color=color_transistor,label="Messwerte Emitterschaltung",marker="x")
    ax.scatter(x_data2,y_data2,color=color_kaskode,label="Messwerte Kaskodenschaltung",marker="x")

    ### v_0 plotten:
    ax.axhline(y=line_transistor,color=color_transistor, linewidth=1, label=r"$v_0$ Emitterschaltung")
    ax.axhline(y=line_kaskode,color=color_kaskode, linewidth=1, label=r"$v_0$ Kaskodenschaltung")
    #ax.axhline(y=line_transistor-3,color=color_transistor,linestyle=":")
    #ax.axhline(y=line_kaskode-3,color=color_kaskode,linestyle=":")


    ### Gerade plotten Emitterschaltung:
    x_data_fit1 = np.array(x_data1[-4:])
    y_data_fit1 = np.array(y_data1[-4:])

    # Berechne die Steigung und den y-Achsenabschnitt der Regressionsgeraden
    coefficients = np.polyfit(x_data_fit1, y_data_fit1, 1)
    slope, intercept = coefficients

    # Die gewünschten y-Werte, für die wir x-Werte berechnen wollen
    y_min = 0
    y_max = line_transistor

    # Berechne die x-Werte, bei denen die Gerade y_min und y_max schneidet
    x_min = (y_min - intercept) / slope
    x_max = (y_max - intercept) / slope

    # Regressionsgerade im Bereich zwischen den y-Werten zeichnen
    ax.plot([x_min, x_max], [y_min, y_max], color_transistor, linestyle=':', label='')



    ### Gerade plotten Kaskodenschaltung:
    x_data_fit2 = np.array(x_data2[-4:])
    y_data_fit2 = np.array(y_data2[-4:])

    # Berechne die Steigung und den y-Achsenabschnitt der Regressionsgeraden
    coefficients = np.polyfit(x_data_fit2, y_data_fit2, 1)
    slope, intercept = coefficients

    # Die gewünschten y-Werte, für die wir x-Werte berechnen wollen
    y_min = 0
    y_max = line_transistor

    # Berechne die x-Werte, bei denen die Gerade y_min und y_max schneidet
    x_min = (y_min - intercept) / slope
    x_max = (y_max - intercept) / slope

    # Regressionsgerade im Bereich zwischen den y-Werten zeichnen
    ax.plot([x_min, x_max], [y_min, y_max], color_kaskode, linestyle=':', label='')


    ### Layout:
    ax.set_xlim(1,10)
    ax.set_xlabel(r"$\log(f)$")
    ax.set_ylabel(r"$20 log(v)$")
    ax.set_ylim(0,18)
    
    ax.grid(True, which="major", linestyle="-")
    plt.legend()
    plt.savefig("../plot/4.pdf",dpi=250)


data1 = get_data_pd('../data/4a.csv')
data1 = process_data(data1, '../data/4a_out.csv')
data2 = get_data_pd('../data/4b.csv')
data2 = process_data(data2, '../data/4b_out.csv')
plot_data(data1,data2)