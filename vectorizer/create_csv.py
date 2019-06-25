#convert all documents in data/*/* into vectors and write to csv

import glob
import sys
import csv
import numpy as np
from vectorizer import vectorizer

def createCSV(out_filename, addrs, labels, dim):
    # create a vectorizer
    v = vectorizer(dim)
    with open(out_filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        header = ["File", "Priority"]
        for x in range(dim):
            header.append(x)
        writer.writerow(header)

        for i in range(len(addrs)):
            # print how many documents are saved every 1000 images
            if not i % 1000:
                print('Train data: {}/{}'.format(i, len(addrs)))
                sys.stdout.flush()
            # Load the image
            str = v.read_txt_file(addrs[i])
            h, wkp, wkm = v.vectorize(str)
            print(h)
            if str is None:
                continue
            row = [addrs[i]]
            row.append(labels[i])
            for j in range(len(h)):
                row.append(h[j])
            writer.writerow(row)


dim = 100
document_path = 'data/*/*.txt'
# read addresses and labels from the 'train' folder
addrs = glob.glob(document_path)

# read labels from directory names
# i.e. priority 1 files are in dir 1/
labels = [0 if 'Red' in addr else 1 if 'Yellow' in addr else 2 if 'Green' in addr else -1 for addr in addrs]  # 0 = Cat, 1 = Dog
#for i in range(len(labels)):
#    print(labels[i])
createCSV('data.csv', addrs, labels, dim)
