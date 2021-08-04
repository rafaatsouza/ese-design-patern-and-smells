import os
import numpy as np
import pandas as pd


class Analyzer:
    def __init__(self, filepath):
        if not filepath:
            raise Exception('Empty filepath')

        if not os.path.isfile(filepath):
            raise Exception('Invalid filepath')

        if not filepath.endswith('.csv'):
            raise Exception('Invalid filepath')

        self.dataframes = self.__get_dataframes(filepath)
        self.summary = None

    def __get_dataframes(self, filepath):
        dataframe = pd.read_csv(filepath, sep=';', header=0)

        dataframe.drop('system', inplace=True, axis=1)
        dataframe.drop('cbo', inplace=True, axis=1)
        dataframe.drop('wmc', inplace=True, axis=1)
        dataframe.drop('dit', inplace=True, axis=1)
        dataframe.drop('rfc', inplace=True, axis=1)
        dataframe.drop('nom', inplace=True, axis=1)
        dataframe.drop('loc', inplace=True, axis=1)

        dataframes = {}

        design_pattern_labels = ['Bridge', 'Composite', 'Chain of Responsibility',
                                 'Template Method', 'Factory Method', 'Prototype']
        design_patterns = ['Bridge', 'Composite', 'ChainOfResponsibility',
                           'TemplateMethod', 'FactoryMethod', 'Prototype']

        for i in range(len(design_patterns)):
            dataframes[design_pattern_labels[i]] = dataframe.copy()
            dataframes[design_pattern_labels[i]] = dataframes[design_pattern_labels[i]][dataframes[design_pattern_labels[i]][design_patterns[i]] == 1]
            for _design_pattern in design_patterns:
                dataframes[design_pattern_labels[i]].drop(
                    _design_pattern, inplace=True, axis=1)

        del design_patterns
        del dataframe

        return dataframes

    def run(self):
        smells_columns = ['GC', 'RPB', 'FE', 'LM']
        smells = ['God Class', 'Refused Bequest',
                  'Feature Envy', 'Long Method']

        smells_average = {}
        self.summary = {
            'patterns': {},
            'smells': {}
        }                

        for design_pattern, dataframe in self.dataframes.items():
            classes = dataframe.shape[0]

            smelly_series = dataframe.apply(
                lambda x: self.__has_any_smell(x, smells_columns), axis=1)
            smelly_classes = len(smelly_series[smelly_series == True].index)

            self.summary['patterns'][design_pattern] = {}

            for i in range(len(smells)):
                smell_freq_in_all = (dataframe[smells_columns[i]].sum())/classes

                if len(smells_average) == 0 or smells_columns[i] not in smells_average:
                    smells_average[smells_columns[i]] = [smell_freq_in_all]
                else:
                    smells_average[smells_columns[i]].append(smell_freq_in_all)

                self.summary['patterns'][design_pattern][smells[i]] = {
                    'freq_in_all': smell_freq_in_all,
                    'freq_in_smelly': ((dataframe[smells_columns[i]].sum())/smelly_classes)
                }

            self.summary['patterns'][design_pattern]['classes'] = classes
            self.summary['patterns'][design_pattern]['smelly_classes'] = smelly_classes

        for i in range(len(smells)):
            self.summary['smells'][smells[i]] = {
                'average': np.mean(smells_average[smells_columns[i]]),
                'standard_deviation': np.std(smells_average[smells_columns[i]])
            }

        del smells_average
        del smell_freq_in_all

        del classes
        del smelly_classes
        del smelly_series
        del smells_columns
        del smells
        del self.dataframes

    def show(self):
        if self.summary is None:
            raise ValueError(
                'Summary not computed. Call the "run" method first')

        for design_pattern, info in self.summary['patterns'].items():
            print('---------------')
            print('{} design pattern'.format(design_pattern))
            print('{} classes, {} smelly classes'.format(
                info['classes'], info['smelly_classes']))

            for smell, data in [(x, y) for x, y in info.items() if x not in ['classes', 'smelly_classes']]:
                print('   >> {} occurrences across all classes: {}'.format(
                    smell, data['freq_in_all']))
                print('   >> {} occurrences across all smelly classes: {}'.format(
                    smell, data['freq_in_smelly']))

            print('---------------\n')

        for smell, info in self.summary['smells'].items():
            print('---------------')
            print('{} bad smell:'.format(smell))
            print('{} average'.format(info['average']))
            print('{} standard deviation'.format(info['standard_deviation']))
            print('\n---------------\n')

    def __has_any_smell(self, row, smells):
        for smell in smells:
            if row[smell] == 1:
                return True
        return False
