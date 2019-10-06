import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('-s', '--season', nargs='+', type=str,dest='season',default=['2019'], help='input season type')

args = parser.parse_args()

print(args.season)
