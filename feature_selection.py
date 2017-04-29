import tensorflow as tf
import numpy as np
import re

x = tf.placeholder(tf.float32, [None, 17815])

W = tf.Variable(tf.zeros([17815, 5]))
b = tf.Variable(tf.zeros([5]))

with tf.Session() as sess:
    print "Are we working?"

def loadExpressionData():
    n_samples = 0  # the number of labeled data samples
    with open('BRCA.exp.466.med.txt', 'rb') as expressionDataFile:
        first = True
        for data_row in expressionDataFile:
            if first:
                header_list = re.split(r'\t+', data_row.rsplit('\t'))

                pass
            else:
                pass
    pass