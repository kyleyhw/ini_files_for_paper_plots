import pandas as pd
import numpy as np
import h5py

class DataLoader:
    def __init__(self, filename):
        file = h5py.File(filename, 'r')
        # print(file['tov_seq_table'].keys())

        solar_mass = 1.989e30

        self.ms = np.array(file['tov_seq_table']['mass_bar']) / solar_mass
        self.lambdas = np.array(file['tov_seq_table']['lambda_tidal'])


        # file = pd.read_csv(filename, delimiter=' ').to_numpy().T
        #
        # c = 2.9979e+8
        # G = 6.6743e-11
        #
        # self.ms = file[0] * (c ** 2) / G
        # self.lambdas = file[1]