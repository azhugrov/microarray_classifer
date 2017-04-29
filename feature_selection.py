import tensorflow as tf
import numpy as np
import re

def loadExpressionData():
    samples_size = 0  # the number of labeled data samples
    samples_names = []
    training_samples = []
    gene_features = []
    with open('BRCA.exp.466.med.txt', 'rb') as expressionDataFile:
        file_line_number = 1
        for data_row in expressionDataFile:
            if file_line_number == 1:
                header_list = re.split(r'\t', data_row.rstrip('\t'))
                samples_size = len(header_list) - 1
                assert samples_size > 1, "number of samples should be greater than one"
                samples_names = [header_list[i] for i in range(1, len(header_list))]
            else:
                if len(training_samples) == 0:
                    for sample_index in range(0, samples_size):
                        training_samples.append([])
                data_list = re.split(r'\t', data_row.rstrip('\t'))
                assert len(data_list) == samples_size + 1, "All data row should have the same dimensions at line number {}".format(file_line_number)
                gene_features.append(data_list[0].strip())
                for sample_index in range(0, samples_size):
                    if data_list[sample_index + 1]:
                        value = float(data_list[sample_index + 1])
                    else:
                        value = None
                    training_samples[sample_index].append(value)
            file_line_number += 1
    return (gene_features, samples_names, training_samples)

x = tf.placeholder(tf.float32, [None, 17815])

W = tf.Variable(tf.zeros([17815, 5]))
b = tf.Variable(tf.zeros([5]))

with tf.Session() as sess:
    gene_features, samples_names, training_samples = loadExpressionData()
    print "Samples size: {} \n".format(len(samples_names))
    print "Gene features size: {} \n".format(len(gene_features))
    print "Samples\Genes\t", "\t".join(gene_features), "\n"
    sample_index = 0
    for sample in training_samples:
        print samples_names[sample_index], "\t"
        for feature_index in range(0, len(gene_features)):
            print training_samples[sample_index][feature_index], "\t"
        print "\n"
        sample_index += 1
