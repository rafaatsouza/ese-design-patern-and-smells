import argparse
from parser import Parser
from parser import Systems

parser = argparse.ArgumentParser(description="Arguments Description")

parser.add_argument('--tool', type=Systems, default=None,
                    required=True, choices=list(Systems), help='Tool')
parser.add_argument('--file', default=None,
                    required=True, help='File path')

args = parser.parse_args()

parser = Parser(args.tool, args.file)
parser.getParsedOutput()
