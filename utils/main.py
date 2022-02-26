# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import re
import json

import keras
import nltk
import sklearn
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
    training_seq = tokenizer.texts_to_sequences(command_data['commands'])
    input_training_data = tf.keras.preprocessing.sequence.pad_sequences(training_seq, dtype='int32')
    le = sklearn.preprocessing.LabelEncoder()
    output_training_data = le.fit_transform(command_data['commands'])

    i = keras.Input(shape=(input_training_data.shape[1],))
    x = keras.layers.Embedding(len(tokenizer.word_index)+1, 10)(i)
    x = keras.layers.LSTM(10, return_sequences=True)(x)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(le.classes_.shape[0], activation="softmax")(x)
    model = keras.Model(i, x)
    model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
    train = model.fit(input_training_data, output_training_data, epochs=300)

    scanned_text_input = input("ENTER YOUR COMMAND: ")
    # NEED TO PROCESS THE INPUT
    '''
    TODO
        - Get the input processing.
        - Refactor the code into a proper OOP format
        - Add the YT API as a sub-repository
        - Research on Discord API
        - Data pipeline (similar to previous one but this time, iterate over the past values and merge to prevent 
        discontigouity)
    '''

    print(scanned_text_input)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
