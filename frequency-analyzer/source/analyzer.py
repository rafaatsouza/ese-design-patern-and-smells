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

        self.datasets = self.get_datasets(filepath)

    def get_datasets(self, filepath):
        dataset = pd.read_csv(filepath, sep=';', header=0)

        dataset.drop('system', inplace=True, axis=1)
        dataset.drop('cbo', inplace=True, axis=1)
        dataset.drop('wmc', inplace=True, axis=1)
        dataset.drop('dit', inplace=True, axis=1)
        dataset.drop('rfc', inplace=True, axis=1)
        dataset.drop('nom', inplace=True, axis=1)
        dataset.drop('loc', inplace=True, axis=1)

        design_patterns = ['Bridge', 'Composite', 'ChainOfResponsibility',
                           'TemplateMethod', 'FactoryMethod', 'Prototype']
        datasets = {}

        for design_pattern in design_patterns:
            datasets[design_pattern] = dataset.loc[dataset[design_pattern] == 1]
            for _design_pattern in design_patterns:
                datasets[design_pattern].drop(
                    _design_pattern, inplace=True, axis=1)

        del design_patterns
        del dataset

        return datasets

    def run(self):
        for key, value in self.datasets.items():
            print('Dataset for the {} pattern\n'.format(key))
            print(self.datasets[key])
