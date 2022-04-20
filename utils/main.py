# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import re
import json
import keras
import nltk
import string
import sklearn
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import keras_preprocessing.sequence

class NLPModel:
    def __init__(self, dff=None, col_name='commands'):
        self.comm_df = dff
        self.model = None
        self.le = None
        self.tokenizer = None
        self.sequences = None
        self.input_training_data = None
        self.output_training_data = None
        self.epochs = 350

        if dff is not None or col_name is not None:
            self.process_dataframe_data(dff, col_name)
            self.init_model()

    def process_dataframe_data(self, df, col):
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=1000)
        # command_data['commands'] - this represents a data frame that containing the command within one
        # column ('commands') and the associated "type" (could be music, weather, radio, etc.)

        self.tokenizer.fit_on_texts(df[col])

        self.sequences = self.tokenizer.texts_to_sequences(df[col])

        self.input_training_data = tf.keras.preprocessing.sequence.pad_sequences(self.sequences, dtype='int32')
        self.le = sklearn.preprocessing.LabelEncoder()
        self.output_training_data = self.le.fit_transform   (df[col])

    def init_model(self):
        i = keras.Input(shape=(self.input_training_data.shape[1],))
        x = keras.layers.Embedding(len(self.tokenizer.word_index) + 1, 10)(i)
        x = keras.layers.LSTM(10, return_sequences=True)(x)
        x = keras.layers.Flatten()(x)
        x = keras.layers.Dense(self.le.classes_.shape[0], activation="softmax")(x)
        self.model = keras.Model(i, x)
        self.model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
        train = self.model.fit(self.input_training_data, self.output_training_data, epochs=self.epochs)

    def process_text(text):
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text

    def vectorize_text(self, text):
        text_list = [text]
        text = self.tokenizer.texts_to_sequences(text_list)
        text = np.array(text).reshape(-1)
        text = keras_preprocessing.sequence.pad_sequences([text], self.input_training_data.shape[1])
        return self.optimize_output(text)

    def optimize_output(self, text):
        pred = self.model.predict(text)
        pred = pred.argmax()
        return self.le.inverse_transform([pred])[0]

    def classify_command(self, text, cmodel):
        assert self.comm_df is not None, \
            "Please enter a valid data frame based on the command model class."
        return cmodel.input_to_command(self.vectorize_text(NLPModel.process_text(text)))


class CommandModel:
    def __init__(self, file_path):
        self.data_fp = file_path
        self.inputs_to_comm = {}
        self.all_commands = []
        self.all_inputs = []
        self.training_data = None
        self.df = None

        self.open_json(file_path)
        self.init_inputs_mapping()

        for i in self.training_data['commands']:
            outputs[i['type']] = i['output']
            for j in i['input']:
                self.all_inputs.append(j)
                self.all_commands.append(i['type'])

        self.configure_dataframe()

    def init_inputs_mapping(self):
        assert self.data_fp is not None, \
            "Can not configure the mapping from inputs to commands. Please configure a non-None filepath."
        temp = {}
        with open(self.data_fp, 'r') as f:
            temp = json.load(f)
            for objs in temp['commands']:
                for comm in objs['input']:
                    self.inputs_to_comm[comm] = objs["type"]

    def configure_dataframe(self):
        self.df = pd.DataFrame({"commands": self.all_inputs, "type": self.all_commands})
        self.df = self.df.reset_index()
        self.df['commands'].apply(lambda x: re.sub(r'[^\w\s]', '', x))

    def open_json(self, file_path):
        assert self.data_fp is not None, \
            "Please configure a valid non-null file path."
        with open(self.data_fp) as command_variants:
            self.training_data = json.load(command_variants)

    def input_to_command(self, text):
        assert text in list(self.inputs_to_comm.keys()), \
            "Input was not found as a key within a key-value pair."
        return self.inputs_to_comm[text]

    def set_filepath(self, fp):
        self.data_fp = fp

    def get_filepath(self):
        return self.data_fp

    def get_dataframe(self):
        return self.df


command_types = [] # Represents lists of all possible current commands. There are duplicates within this list
inputs = [] # List of all possible inputs
outputs = {} # List of dictionaries. In the form {command_type:[input1, input2, ...]}
inputs_to_commands = {} # Mapping of the inputs to commands
command_data = 0 # Dataframe representing the commands and their type


def init_inputs_to_comm_map():
    global inputs_to_commands
    temp = {}
    with open('commands.json', 'r') as f:
        temp = json.load(f)
        for objs in temp['commands']:
            for comm in objs["input"]:
                inputs_to_commands[comm] = objs["type"]


def reshape_to_dataframe(mapping):
    global command_data
    command_data = pd.DataFrame(mapping)
    command_data = command_data.reset_index()
    command_data['commands'].apply(lambda x: re.sub(r'[^\w\s]', '', x))


def process_input_chars(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


def vectorize_string(text, tokenizer, shape):
    text_list = [text]
    text = tokenizer.texts_to_sequences(text_list)
    print("LINE 40", text)
    text = np.array(text).reshape(-1)
    print("LINE 41", text)
    text = tf.keras.preprocessing.sequence.pad_sequences(text_list, shape)
    return text


def get_response(text, mm, encoder, tokenizer, shape):
    text = process_input_chars(text)
    print(text)
    text = vectorize_string(text, tokenizer, shape)
    response = mm.predict(text)
    opt = response.argmax()
    return encoder.inverse_transform([opt])[0]


def main():
    with open('commands.json') as command_variants:
        training_data = json.load(command_variants)

    init_inputs_to_comm_map()

    for i in training_data['commands']:
        outputs[i['type']] = i['output']
        for j in i['input']:
            inputs.append(j)
            command_types.append(i['type'])

    reshape_to_dataframe({"commands": inputs, "type": command_types})

    '''
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=1000)
    tokenizer.fit_on_texts(command_data['commands'])
    training_seq = tokenizer.texts_to_sequences(command_data['commands'])
    input_training_data = tf.keras.preprocessing.sequence.pad_sequences(training_seq, dtype='int32')
    le = sklearn.preprocessing.LabelEncoder()
    output_training_data = le.fit_transform(command_data['commands'])

    i = keras.Input(shape=(input_training_data.shape[1],))
    x = keras.layers.Embedding(len(tokenizer.word_index) + 1, 10)(i)
    x = keras.layers.LSTM(10, return_sequences=True)(x)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(le.classes_.shape[0], activation="softmax")(x)
    model = keras.Model(i, x)
    model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
    train = model.fit(input_training_data, output_training_data, epochs=350)

    scanned_text_input = input("ENTER YOUR COMMAND: ")
    predicted_input = vectorize_input(process_text(scanned_text_input), model, le, tokenizer, input_training_data.shape[1])
    print("The detected command is: ", inputs_to_commands[predicted_input]) 
    '''


    '''
    class Commands: 
        Instance Variables:
        - self.data_path -- this is the path to the JSON file
        - self.inputs_to_comm -- this is a mapping of a particular classified input into a command
        - self.all_commands -- list of all of the possible commands. Currently, there are duplicates within this array
        - self.all_inputs - list representing all possible inputs described from the JSON training file
        - self.training_data - JSON version of data
        - self.data_df - dataframe of training data
        
        Methods: 
        - def configure_dataframe(self):
        - def process_JSON
        - def get_command(input) # Will return the command associated with the given input. 
    '''

    '''
    TODO
        - Refactor the code into a proper OOP format
        - Add the YT API as a sub-repository
        - Research on Discord API
        - Data pipeline (similar to previous one but this time, iterate over the past values and merge to prevent 
        discontinuity) (maybe have it in SQL)
    '''


def process_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


def vectorize_input(text, model, le, tokenizer, shape):
    text_list = [text]
    text = tokenizer.texts_to_sequences(text_list)
    text = np.array(text).reshape(-1)
    text = keras_preprocessing.sequence.pad_sequences([text], shape)
    return optimize_output(text, model, le)


def optimize_output(text, model, le):
    prediction = model.predict(text)
    prediction = prediction.argmax()
    return le.inverse_transform([prediction])[0]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
