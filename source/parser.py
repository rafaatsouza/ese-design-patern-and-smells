import os.path

from xml.dom import minidom
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
            raise Exception('Empty filepath')

        if not os.path.isfile(filepath):
            raise Exception('Invalid filepath')

        if not filepath.endswith('.xml'):
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
        classes = []

        xml = minidom.parse(filepath)
        patternName = xml.getElementsByTagName(
            'PatternName')[0].firstChild.data

        anchors = xml.getElementsByTagName('AnchorsInstance')
        roles = xml.getElementsByTagName('RoleInstance')

        for anchor in anchors:
            if anchor.attributes['value'].value not in classes:
                classes.append(anchor.attributes['value'].value)

        for role in roles:
            if role.attributes['value'].value not in classes:
                classes.append(role.attributes['value'].value)

        self.printOutput('jasper', patternName, classes)

    def parseJFree(self, filepath):
        raise Exception('Parse from JFreeChart output file is not implemented')

    def parseJHot(self, filepath):
        raise Exception('Parse from JHotDraw output file is not implemented')

    def parseJMeter(self, filepath):
        raise Exception('Parse from JMeter output file is not implemented')

    def parseStruts(self, filepath):
        raise Exception('Parse from Struts output file is not implemented')

    def printOutput(self, tool, patternName, classes):
        print('tool;pattern;class')
        for _class in classes:
            print('{};{};{}'.format(tool, patternName, _class))
