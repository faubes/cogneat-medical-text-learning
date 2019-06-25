import pandas as pd
import numpy as np
import sys
import time
import pickle
import argparse

import keras
from keras.layers import Flatten, Dense, Input
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model
from keras.models import Sequential
from keras.models import model_from_json

datafile = "noteevents5000.csv"
max_words=10000
classes = ['low', 'medium', 'high']
num_classes=3
num_epochs=3
batch_size=128

def load_tokenizer():
    try:
        # loading the tokenizer
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        print("Loaded tokenizer from disk")
    except:
        sys.exit("error loading tokenizer from disk")

    return tokenizer

def load_text_file(filename):
    try:
        with open(filename, 'r') as handle:
            text = handle.read()
    except:
        sys.exit("error loading test file from disk")
    return text

def train():
    print("Loading data")
    # load the csv into a dataframe
    df = pd.read_csv(datafile, header=None)

    # extract clinical notes from 5th column
    x_train = np.asarray(df[5])

    print("Building tokenizer")
    # build a tokenizer and fit to corpus
    tokenizer = Tokenizer(num_words=max_words)
    print("Fitting on texts")
    tokenizer.fit_on_texts(x_train)

    # convert texts to vectors using tokenizer
    x_train = tokenizer.texts_to_matrix(x_train, mode='tfidf')

    # assign random labels
    y_train = np.random.choice([0,1,2], size=len(x_train), p=[0.4, 0.3, 0.3])
    y_train = keras.utils.to_categorical(y_train, num_classes)

    model = Sequential()
    model.add(Dense(512, input_shape=(max_words, ), activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])

    start_fit = time.time()
    history = model.fit(x_train, y_train, epochs=num_epochs, batch_size=batch_size, verbose=1)
    #result = model.evaluate(x_test, y_test)
    fit_time = time.time() - start_fit

    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk")

    #save the tokenizer
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("Saved tokenizer to disk")

def test(filename):

    print("Loading model to test on file {}".format(filename))
    try:
        # load json and create model
        with open('model.json', 'r') as handle:
            loaded_model_json = handle.read()

        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("model.h5")
        print("Loaded model from disk")
        loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    except:
        sys.exit("error loading model from disk")

    tokenizer = load_tokenizer()

    text = load_text_file(filename)

    print("Converting input to vector")
    # convert text to predict to vector
    vector = tokenizer.texts_to_matrix([text], mode='tfidf')
    vector = pad_sequences(vector, max_words)

    # use loaded model to make a prediction
    prediction = loaded_model.predict_classes(vector)
    print("Algorithm predicts {} priority".format(classes[np.asscalar(prediction)]))
#    return loaded_model, tokenizer, text, vector

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CogNeat Text Classification')
    parser.add_argument('--train', action='store_true', default=False, help='Train and save model (default: false)')
    parser.add_argument('--predict', type=str, metavar='filename', help='Use trained model to predict file')
    args = parser.parse_args()

    if args.train:
        train()

    if args.predict:
        test(args.predict)
