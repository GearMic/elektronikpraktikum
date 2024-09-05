import numpy as np
import pandas as pd

dateiname = "1a.csv"
data = pd.read_csv(dateiname)
data.columns = data.columns.str.strip()

#print(data.columns)
U_E = np.array(data["U_E/V_SS"])
U_B = np.array(data["U_B/V_SS"])

verstärkung = np.round(U_E/U_B,2)

data["v"]=verstärkung

neuer_dateiname = "1a_auswertung.csv"
data.to_csv(neuer_dateiname, index=False)