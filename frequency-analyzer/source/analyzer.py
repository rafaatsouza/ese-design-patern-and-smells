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

        self.summary = {}

        for design_pattern, dataframe in self.dataframes.items():
            classes = dataframe.shape[0]

            smelly_series = dataframe.apply(
                lambda x: self.__has_any_smell(x, smells_columns), axis=1)
            smelly_classes = len(smelly_series[smelly_series == True].index)

            self.summary[design_pattern] = {}

            for i in range(len(smells)):
                self.summary[design_pattern][smells[i]] = {
                    'freq_in_all': ((dataframe[smells_columns[i]].sum())/classes),
                    'freq_in_smelly': ((dataframe[smells_columns[i]].sum())/smelly_classes)
                }

            self.summary[design_pattern]['classes'] = classes
            self.summary[design_pattern]['smelly_classes'] = smelly_classes

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

        for design_pattern, info in self.summary.items():
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

    def __has_any_smell(self, row, smells):
        for smell in smells:
            if row[smell] == 1:
                return True
        return False
