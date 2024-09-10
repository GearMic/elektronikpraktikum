import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


def get_data_pd(filename):
    return pd.read_csv(filename, sep=',', skipinitialspace=True)

def add_data(list, data):
    list.append(data)
    return list

def plot_data(data_list, filename):

    color = ['r','b','g','orange']
    range = np.array([[0,7],[7,None],[-2,None]]) # range der Daten für Gradenfit des linearen Abfalls
    verstärkung = [11,101,2]

    fig, ax = plt.subplots()

    counter = 0
    for data in data_list[:-1]:
        x_data = np.log10(1000 * data["f/kHz"])
        y_data = 20 * np.log10(data["v"])
        y_err = np.sqrt(20 * data["v_err"]/(data["v"]*np.log(10)) * 20 * data["v_err"]/(data["v"]*np.log(10)))
        max_value = max(y_data)
        ### Messwerte plotten:
        #ax.errorbar(x_data,y_data,yerr=y_err,color=color[counter],linestyle='None',label="",marker="x")
        ax.scatter(x_data,y_data,color=color[counter],linestyle='None',label="",marker="x")
        ### v_0 & v_grenz plotten:
        ax.axhline(y=max_value,color=color[counter], linewidth=1, label='')
        ax.axhline(y=max_value-3,color=color[counter],linestyle="--")

        ### Gerade plotten:
        x_data_fit = np.array(x_data[range[counter,0]:range[counter,1]])
        y_data_fit = np.array(y_data[range[counter,0]:range[counter,1]])

        # Berechne die Steigung und den y-Achsenabschnitt der Regressionsgeraden
        coefficients = np.polyfit(x_data_fit, y_data_fit, 1)
        slope, intercept = coefficients

        # Die gewünschten y-Werte, für die wir x-Werte berechnen wollen
        y_min = 0
        y_max = max_value

        # Berechne die x-Werte, bei denen die Gerade y_min und y_max schneidet
        x_min = (y_min - intercept) / slope
        x_max = (y_max - intercept) / slope

        # Regressionsgerade im Bereich zwischen den y-Werten zeichnen
        ax.plot([x_min, x_max], [y_min, y_max], color=color[counter], linestyle=':', label='')

        counter += 1

    for data in data_list[-1:]:
        print(2)
        x_data = np.log10(1000 * data["f/Hz"])
        y_data = 20 * np.log10(data["v"])
        y_err = np.sqrt(20 * data["v_err"]/(data["v"]*np.log(10)) * 20 * data["v_err"]/(data["v"]*np.log(10)))
        max_value = max(y_data)
        ### Messwerte plotten:
        #ax.errorbar(x_data,y_data,yerr=y_err,color=color[counter],linestyle='None',label="",marker="x")
        ax.scatter(x_data,y_data,color=color[counter],linestyle='None',label="",marker="x")
        

    ### Layout:
    ax.set_xlabel(r"$\log(f)$")
    ax.set_ylabel(r"$20 log(v)$")
    ax.set_ylim(0,)
    
    ax.grid(True, which="major", linestyle="-")

    ### Handels:
    red = mlines.Line2D([], [], color='r', marker='o',linestyle='None', label=r'$v=$'+str(verstärkung[0]))
    blue = mlines.Line2D([], [], color='b', marker='o', linestyle='None', label=r'$v=$'+str(verstärkung[1]))
    green = mlines.Line2D([], [], color='g', marker='o', linestyle='None', label=r'$v=$'+str(verstärkung[2]))
    marker = mlines.Line2D([], [], color='gray', marker='x', linestyle='None', label='Messwerte')
    line = mlines.Line2D([], [], color='gray', linestyle='-', label=r'$v_0$')
    dashed_line = mlines.Line2D([], [], color='gray', linestyle='--', label=r'$v_0-3dB$')
    dotted_line = mlines.Line2D([], [], color='gray', linestyle=':', label='Regression')

    ax.legend(handles=[blue,red,green,marker,line,dashed_line, dotted_line])
    plt.savefig(filename,dpi=250)


# Programm:
data_list = []
data = get_data_pd('../data/1a.csv')
data_list = add_data(data_list, data)
data = get_data_pd('../data/1b.csv')
data_list = add_data(data_list, data)
data = get_data_pd('../data/1c.csv')
data_list = add_data(data_list, data)
data = get_data_pd('../data/1e.csv')
data_list = add_data(data_list, data)
print(1)
plot_data(data_list,'../plot/1.pdf')