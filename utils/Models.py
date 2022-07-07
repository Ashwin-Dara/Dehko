import os

# Disabling logging warnings from Tensorflow to clean debugging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Libraries for handling parsing of commands and metadata storage
import re
import json

# Relevant ML/NLP libraries.
import nltk
import keras
import keras_preprocessing.sequence
import tensorflow as tf
import sklearn

# Importing relevant math libraries.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Serialization and file stream libraries
import dill
import string
from os.path import exists


class NLPModel:
    def __init__(self, comm_model=None, col_name='commands'):
        self.comm_model = comm_model
        if self.comm_model is None:
            return
        self.comm_df = self.comm_model.get_dataframe()
        self.model = None
        self.le = None
        self.tokenizer = None
        self.sequences = None
        self.input_training_data = None
        self.output_training_data = None
        self.epochs = 350

        if self.comm_df is not None or col_name is not None:
            self.process_dataframe_data(self.comm_df, col_name)
            self.init_model()

    def process_dataframe_data(self, df, col):
        self.tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=1000)
        # command_data['commands'] - this represents a data frame that containing the command within one
        # column ('commands') and the associated "type" (could be music, weather, radio, etc.)

        self.tokenizer.fit_on_texts(df[col])

        self.sequences = self.tokenizer.texts_to_sequences(df[col])

        self.input_training_data = tf.keras.preprocessing.sequence.pad_sequences(self.sequences, dtype='int32')
        self.le = sklearn.preprocessing.LabelEncoder()
        self.output_training_data = self.le.fit_transform(df[col])

    def init_model(self):
        i = keras.Input(shape=(self.input_training_data.shape[1],))
        x = keras.layers.Embedding(len(self.tokenizer.word_index) + 1, 10)(i)
        x = keras.layers.LSTM(10, return_sequences=True)(x)
        x = keras.layers.Flatten()(x)
        x = keras.layers.Dense(self.le.classes_.shape[0], activation="softmax")(x)
        self.model = keras.Model(i, x)
        self.model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
        train = self.model.fit(self.input_training_data, self.output_training_data, epochs=self.epochs)

    def process_text(self, text):
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

    def classify_command(self, text):
        assert self.comm_df is not None, \
            "Please enter a valid data frame based on the command model class."
        processed = self.process_text(text)
        vectorized = self.vectorize_text(processed)
        return self.comm_model.input_to_command(vectorized)

    def get_command_model(self):
        return self.comm_model


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


command_types = []  # Represents lists of all possible current commands. There are duplicates within this list
inputs = []  # List of all possible inputs
outputs = {}  # List of dictionaries. In the form {command_type:[input1, input2, ...]}
inputs_to_commands = {}  # Mapping of the inputs to commands
command_data = 0  # Dataframe representing the commands and their type


def init_inputs_to_comm_map():
    global inputs_to_commands
    temp = {}
    with open('settings.JSON', 'r') as f:
        temp = json.load(f)
        for objs in temp['commands']:
            for comm in objs["input"]:
                inputs_to_commands[comm] = objs["type"]


def reshape_to_dataframe(mapping):
    global command_data
    command_data = pd.DataFrame(mapping)
    command_data = command_data.reset_index()
    command_data['commands'].apply(lambda x: re.sub(r'[^\w\s]', '', x))


def main(needs_training=False):
    print("$$$ DEBUG: Models.py, Line 178. Printing CWD", os.getcwd())
    if not exists('dumps/optimized_model') or needs_training:
        nn_classifier = None

        with open('settings.JSON') as command_variants:
            training_data = json.load(command_variants)

        init_inputs_to_comm_map()

        for i in training_data['commands']:
            outputs[i['type']] = i['output']
            for j in i['input']:
                inputs.append(j)
                command_types.append(i['type'])

        reshape_to_dataframe({"commands": inputs, "type": command_types})
        nn_classifier = NLPModel(CommandModel("settings.JSON"))
        with open('dumps/optimized_model', 'wb') as outfile:
            dill.dump(nn_classifier, outfile)
            print("Dumped optimized NN model in ./dumps.")


if __name__ == '__main__':
    main()
