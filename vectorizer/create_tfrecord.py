#convert all documents in data/*/* into vectors and write to TFRecord
#adapted from code by github.com/kalsapuffar found at
# https://github.com/kalaspuffar/tensorflow-data/blob/master/create_dataset.py

from random import shuffle
import glob
import sys
import numpy as np
#import skimage.io as io
import tensorflow as tf
from vectorizer import vectorizer

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
#def _bytes_feature(value):
#    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def createDataRecord(out_filename, addrs, labels, dim):
    # open the TFRecords file
    writer = tf.python_io.TFRecordWriter(out_filename)
    # create a vectorizer
    v = vectorizer(dim)
    for i in range(len(addrs)):
        # print how many documents are saved every 1000 images
        if not i % 1000:
            print('Train data: {}/{}'.format(i, len(addrs)))
            sys.stdout.flush()
        # Load the image
        str = v.read_txt_file(addrs[i])

        label = labels[i]

        if str is None:
            continue

        vector_feature_column = tf.feature_column.numeric_column(key="Hashed Document",
                                                         shape=dim)
        # Create a feature
        feature = {
            'vec': vector_feature_column,
            'label': _int64_feature(label)
        }
        # Create an example protocol buffer
        example = tf.train.Example(features=tf.train.Features(feature=feature))

        # Serialize to string and write on the file
        writer.write(example.SerializeToString())

    writer.close()
    sys.stdout.flush()

dim = 100
document_path = 'data/*/*.txt'
# read addresses and labels from the 'train' folder
addrs = glob.glob(document_path)

# read labels from directory names
# i.e. priority 1 files are in dir 1/
labels = [0 if 'Red' in addr else 1 if 'Yellow' in addr else 2 if 'Green' in addr else -1 for addr in addrs]  # 0 = Cat, 1 = Dog
for i in range(len(labels)):
    print(labels[i])

# to shuffle data
c = list(zip(addrs, labels))
shuffle(c)
addrs, labels = zip(*c)

# Divide the data into 60% train, 20% validation, and 20% test
train_addrs = addrs[0:int(0.6*len(addrs))]
train_labels = labels[0:int(0.6*len(labels))]
val_addrs = addrs[int(0.6*len(addrs)):int(0.8*len(addrs))]
val_labels = labels[int(0.6*len(addrs)):int(0.8*len(addrs))]
test_addrs = addrs[int(0.8*len(addrs)):]
test_labels = labels[int(0.8*len(labels)):]

createDataRecord('train.tfrecords', train_addrs, train_labels, dim)
createDataRecord('val.tfrecords', val_addrs, val_labels, dim)
createDataRecord('test.tfrecords', test_addrs, test_labels, dim)
