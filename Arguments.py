import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--daemonize', type=bool)
parser.add_argument('-v', '--verbose', default=False, type=bool)
parser.add_argument('-c', '--create-user', default=False, type=bool)

