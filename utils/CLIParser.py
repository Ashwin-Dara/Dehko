# Libraries related to CLI creation.
import os
import sys
import argparse

# Library for NN model serialization.
import dill

# Importing relevant project files.
import Models
from ClientCycle import MsgClient
from CliOuputs import *

# Importing libraries for progress bar/spinner.
from progress.bar import ShadyBar
from progress.spinner import Spinner
import threading
import time


# The lower the parameter speed is, the fast that the progress bar animation updates.
def progress_bar_animation(speed):
    bar = ShadyBar("Optimizing Neural Network:", max=speed)
    for i in range(0, speed):
        bar.next()
        time.sleep(0.01)
    Models.main(True)
    bar.finish()
    print("\n\nSuccessfully Retrained the Neural Net!")


# Retrains the model by invoking the main function of models and serializes trained NN.
def retrain_model():
    progress_bar_animation(50)


def main():
    # Loading the trained NN model from the serialized file.
    os.chdir('..')
    os.chdir('..')
    nn = None
    with open('dumps/optimized_model', 'rb') as infile:
        nn = dill.load(infile)

    # Debugging print statement to see the contents of sys.argv
    print("$$$ DEBUG: Contents of sys.argv: ", sys.argv)

    # Not enough arguments were passed for Dehko to run sufficiently.
    if len(sys.argv) <= 1:
        print(no_arguments_input)
        return

    # Checking if Dehko is given the --help or -h command.
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print(help_output)
        return

    # Checking if Dehko is given the --train command.
    if sys.argv[1] == "--train":
        print(training_output)
        retrain_model()
        return

    # Adding the initial arguments to the CLI library.
    parser = argparse.ArgumentParser(
        description="Welcome to Dehko 1.02! Please a description of the command you wish to execute.")
    parser.add_argument('command', metavar='<Command Description>', type=str,
                        help='Description of the command you wish to execute.')

    args, leftovers = parser.parse_known_args()
    print("$$$ DEBUG: Parser.parse_known_args. Args component: ", args.command)
    print(f"$$$ DEBUG: Leftsovers component: ", leftovers)

    if args.command is not None:
        print(f"$$$ DEBUG: LINE 25. General description of command: {args.command} ")
        # args = parser.parse_args()
        # print("Recieved Text: ", args.text)

        # Creating a Message Client Object. This is the object responsible for encompassing everything related to
        # processing messages.
        print("Dehko 1.02")
        spinner = Spinner('Executing Scripts ')
        for i in range(0, 250):
            spinner.next()
            time.sleep(0.01)
        spinner.finish()
        m = MsgClient(nn)
        m.process_message(args.command)


if __name__ == '__main__':
    main()
