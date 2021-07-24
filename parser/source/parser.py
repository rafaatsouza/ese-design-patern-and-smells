import os

from xml.dom import minidom
from enum import Enum


class Tools(Enum):
    JasperReports = 'jasper'
    JFreeChart = 'jfree'
    JHotDraw = 'jhot'
    JMeter = 'jmeter'
    Struts = 'struts'


class Parser:
    def __init__(self, tool, filepath):
        if not isinstance(tool, Tools):
            raise Exception('Invalid tool')

        if not filepath:
            raise Exception('Empty filepath')

        if not os.path.isfile(filepath):
            raise Exception('Invalid filepath')

        if not filepath.endswith('.xml'):
            raise Exception('Invalid filepath')

        tools = {
            Tools.JasperReports: 'JasperReports',
            Tools.JFreeChart: 'JFreeChart',
            Tools.JHotDraw: 'JHotDraw',
            Tools.JMeter: 'JMeter',
            Tools.Struts: 'Struts'
        }

        self.tool = tools[tool]
        self.filepath = filepath

    def printParsedXml(self):
        xml = minidom.parse(self.filepath)
        patternName = xml.getElementsByTagName(
            'PatternName')[0].firstChild.data
            
        classes = self.getClasses(xml)

        self.printOutput(self.tool, patternName, classes)

    def getOutputFilePath(self):
        parts = self.filepath.split('/')
        parts[-1] = 'parsed-{}'.format(parts[-1])
        return '/'.join(parts).replace('.xml', '.csv')

    def getClasses(self, xml):
        classes = []
        anchors = xml.getElementsByTagName('AnchorsInstance')
        roles = xml.getElementsByTagName('RoleInstance')

        if anchors:
            for anchor in anchors:
                if anchor.attributes['value'].value not in classes:
                    classes.append(anchor.attributes['value'].value)

        if roles:
            for role in roles:
                if role.attributes['value'].value not in classes:
                    classes.append(role.attributes['value'].value)

        return classes

    def printOutput(self, tool, patternName, classes):
        with open(self.getOutputFilePath(), 'w') as file:
            file.write('tool;pattern;class\n')
            for _class in classes:
                file.write('{};{};{}\n'.format(tool, patternName, _class))
