import argparse
import dill
from ClientCycle import MsgClient

parser = argparse.ArgumentParser(description="Process some text and classify it.")
parser.add_argument('text', metavar='T', type=str, help='Description of what you wish to do.')


def main():
    nn = None
    with open('dumps/optimized_model', 'rb') as infile:
        nn = dill.load(infile)
        print("Loaded Pickled Model!")
    args = parser.parse_args()
    print("Recieved Text: ", args.text)
    m = MsgClient(nn)
    m.process_message(args.text)


if __name__ == '__main__':
    main()
