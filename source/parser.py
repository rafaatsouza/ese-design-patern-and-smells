from enum import Enum


class Systems(Enum):
    JasperReports = 'jasper'
    JFreeChart = 'jfree'
    JHotDraw = 'jhot'
    JMeter = 'jmeter'
    Struts = 'struts'


class Parser:
    def __init__(self, system, filepath):
        if not isinstance(system, Systems):
            raise Exception('Invalid system')

        if not filepath:
            raise Exception('Invalid filepath')

        methods = {
            Systems.JasperReports: self.parseJasper,
            Systems.JFreeChart: self.parseJFree,
            Systems.JHotDraw: self.parseJHot,
            Systems.JMeter: self.parseJMeter,
            Systems.Struts: self.parseStruts
        }

        self.method = methods[system]
        self.filepath = filepath

    def getParsedOutput(self):
        self.method(self.filepath)

    def parseJasper(self, filepath):
        raise Exception(
            'Parse from JasperReports output file is not implemented')

    def parseJFree(self, filepath):
        raise Exception('Parse from JFreeChart output file is not implemented')

    def parseJHot(self, filepath):
        raise Exception('Parse from JHotDraw output file is not implemented')

    def parseJMeter(self, filepath):
        raise Exception('Parse from JMeter output file is not implemented')

    def parseStruts(self, filepath):
        raise Exception('Parse from Struts output file is not implemented')
