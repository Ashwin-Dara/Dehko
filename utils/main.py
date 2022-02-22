# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import re
import json
import nltk
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

command_types = []
inputs = []
outputs = {}
command_data = 0

def reshape_to_dataframe(mapping):
    global command_data
    command_data = pd.DataFrame(mapping)
    command_data = command_data.reset_index()
    command_data['commands'].apply(lambda x: re.sub(r'[^\w\s]', '', x))


def main():
    with open('commands.json') as command_variants:
        training_data = json.load(command_variants)

    for i in training_data['commands']:
        outputs[i['type']] = i['output']
        for j in i['input']:
            inputs.append(j)
            command_types.append(i['type'])

    reshape_to_dataframe({"commands": inputs, "type": command_types})
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words = 1000)
    tokenizer.fit_on_texts(command_data['commands'])
    # training_data_x = tf.ker



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    print(inputs)
    print(command_types)
    print(command_data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
