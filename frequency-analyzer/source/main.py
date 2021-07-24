import argparse
from analyzer import Analyzer

parser = argparse.ArgumentParser(description="Arguments Description")

parser.add_argument('--file', default=None,
                    required=True, help='File path')

args = parser.parse_args()

analyzer = Analyzer(args.file)
analyzer.run()

analyzer.show()