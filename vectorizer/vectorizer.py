#vectorizer.py
#convert document into vector
import sys
import os
import numpy as np

class vectorizer():

	def __init__(self, n=1000):
		assert n>0, "Need n>0"
		self.n = n

	def read_txt_file(self, filename):
		str = "" # init empty string
		# open file (read only) and read into str
		with open(filename, "r") as f:
			str = f.read()
		return str

	def vectorize(self, str):
		# hashes str into a n-dimensional vector
		# by counting words into buckets
		# requires str
		# returns n dimensional vector v of "word counts"
		# returns work_key_plus, an array of lists of words mapped to +
		# returns work_key_minus, an array of lists of words mapped to -

		v = np.zeros(self.n) # create zero vector of length n
		word_key_plus = [ [] for i in range(self.n) ]
		word_key_minus = [ [] for i in range(self.n) ]
		# print(str) # for testing
		# convert each word into a number
		# increment (or decrement) bucket number in vector
		for word in str.split():
			t = 0
			for idx, c in enumerate(word):
				t += idx*ord(c)
			b = t % self.n
			if (t % 2 == 0):
				v[b] += 1
				if (word not in word_key_plus[b]):
					word_key_plus[b].append(word)
			else:
				v[b] -= 1
				if (word not in word_key_minus[b]):
					word_key_minus[b].append(word)
		return v, word_key_plus, word_key_minus

	def vectorize_test(self, str):
		# hashes str into a n-dimensional vector
		# by counting words into buckets
		# requires str
		# returns n dimensional vector v of "word counts"
		# returns work_key_plus, an array of lists of words mapped to +
		# returns work_key_minus, an array of lists of words mapped to -

		v = np.zeros(self.n) # create zero vector of length n
		word_key_plus = [ [] for i in range(self.n) ]
		word_key_minus = [ [] for i in range(self.n) ]
		# print(str) # for testing
		# convert each word into a number
		# increment (or decrement) bucket number in vector
		for word in str.split():
			print(word)
			t = 0
			for idx, c in enumerate(word):
				print('{}, {}'.format(c, ord(c)))
				t += idx*ord(c)
			b = t % self.n
			if (t % 2 == 0):
				v[b] += 1
				if (word not in word_key_plus[b]):
					word_key_plus[b].append(word)
			else:
				v[b] -= 1
				if (word not in word_key_minus[b]):
					word_key_minus[b].append(word)
			print(b)
		return v, word_key_plus, word_key_minus

def main():
	dim = 100
	assert len(sys.argv) == 2, "Usage: python3 vectorizer filename.txt"
	filepath = sys.argv[1]
	print('Opening file: {}'.format(filepath))
	v = vectorizer(dim)
	str = v.read_txt_file(filepath)
	res, wkp, wkm = v.vectorize(str)

	#print the word key
	for i in range(dim):
		print('{}'.format(i))
		for word in wkp[i]:
			print('{}'.format(word))
		for word in wkm[i]:
			print('{}'.format(word))

	#print the vector
	print(res)

if __name__== "__main__":
	main()
