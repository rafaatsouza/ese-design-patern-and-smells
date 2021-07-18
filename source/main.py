import argparse
from parser import Parser
from parser import Tools

parser = argparse.ArgumentParser(description="Arguments Description")

parser.add_argument('--tool', type=Tools, default=None,
                    required=True, choices=list(Tools), help='Tool')
parser.add_argument('--file', default=None,
                    required=True, help='File path')

args = parser.parse_args()

parser = Parser(args.tool, args.file)
parser.getParsedOutput()
