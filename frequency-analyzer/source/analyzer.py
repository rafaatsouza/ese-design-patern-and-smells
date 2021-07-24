import os
import pandas as pd


class Analyzer:
    def __init__(self, filepath):
        if not filepath:
            raise Exception('Empty filepath')

        if not os.path.isfile(filepath):
            raise Exception('Invalid filepath')

        if not filepath.endswith('.csv'):
            raise Exception('Invalid filepath')

        self.dataset = pd.read_csv(filepath, sep=';', header=0)

        self.dataset.drop('sistema', inplace=True, axis=1)
        self.dataset.drop('cbo', inplace=True, axis=1)
        self.dataset.drop('wmc', inplace=True, axis=1)
        self.dataset.drop('dit', inplace=True, axis=1)
        self.dataset.drop('rfc', inplace=True, axis=1)
        self.dataset.drop('nom', inplace=True, axis=1)
        self.dataset.drop('loc', inplace=True, axis=1)

    def run(self):
        print(self.dataset)
