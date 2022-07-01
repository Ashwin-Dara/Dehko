import os
import argparse
import dill
from ClientCycle import MsgClient

parser = argparse.ArgumentParser(description="Welcome to Dehko 1.02! Please a description of the command you wish to execute.")
parser.add_argument('text', metavar='<Command Description>', type=str, help='Description of the command you wish to execute.')
parser.add_argument('text', metavar='<Links/Command Arguments>', type=str,
                    help='Any additional arguments to go with the commands. Arguments be preceded by "~".')

def main():
    nn = None
    with open('dumps/optimized_model', 'rb') as infile:
        nn = dill.load(infile)
    if parser.parse_args():
        args = parser.parse_args()
        print("Recieved Text: ", args.text)
        m = MsgClient(nn)
        m.process_message(args.text)


if __name__ == '__main__':
    main()
