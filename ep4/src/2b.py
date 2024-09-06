import numpy as np
import pandas as pd

def get_data_pd(filename):
    return pd.read_csv(filename, sep=',', skipinitialspace=True)

def process_data(data, dataFile):
    # data.columns = data.columns.str.strip()

    U_E = np.array(data["U_E/V_SS"])
    U_B = np.array(data["U_B/V_SS"])
    dU = np.array(data["dU/V"])

    v = np.round(U_E/U_B,2)
    dv = np.round(np.sqrt((dU/U_B)*(dU/U_B)+((U_E*dU)/(U_B*U_B))*((U_E*dU)/(U_B*U_B))),2)

    data["v"]=v
    data["dv"]=dv

    data.to_csv(dataFile, index=False)
    return data



data = get_data_pd('ep4/data/2b.csv')
data = process_data(data, 'ep4/data/2b_out.csv')