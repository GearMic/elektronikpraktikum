import numpy as np
import pandas as pd

dateiname = "../data/1a.csv"
data = pd.read_csv(dateiname)
data.columns = data.columns.str.strip()

U_E = np.array(data["U_E/V_SS"])
U_B = np.array(data["U_B/V_SS"])
dU = np.array(data["dU/V"])

verstärkung = np.round(U_E/U_B,2)
dv = np.round(np.sqrt((dU/U_B)*(dU/U_B)+((U_E*dU)/(U_B*U_B))*((U_E*dU)/(U_B*U_B))),2)

data["v"]=verstärkung
data["dv"]=dv

neuer_dateiname = "../data/1a_auswertung.csv"
data.to_csv(neuer_dateiname, index=False)