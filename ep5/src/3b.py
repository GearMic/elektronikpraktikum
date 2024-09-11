import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def get_data_pd(filename):
    return pd.read_csv(filename, sep=',', skipinitialspace=True)

def process_data(data):
    R_2 = np.array(data['R_2/kohm'])
    R_2Err = np.array(data['R_2Err'])
    U_out = np.array(data['U_out/V'])
    U_outErr = np.array(data['U_outErr'])

