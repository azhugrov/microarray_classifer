import tensorflow as tf
import numpy as np
import data_loader
import sys

x = tf.placeholder(tf.float32, [None, 17815])

W = tf.Variable(tf.zeros([17815, 5]))
b = tf.Variable(tf.zeros([5]))

with tf.Session() as sess:
    gene_features, samples_names, training_samples = data_loader.loadExpressionData()
    sys.stdout.write("Samples size: {} \n".format(len(samples_names)))
    sys.stdout.write("Gene features size: {} \n".format(len(gene_features)))
    print "Samples\Genes\t", "\t".join(gene_features)
    sample_index = 0
    for sample in training_samples:
        sys.stdout.write(samples_names[sample_index])
        sys.stdout.write("\t")
        for feature_index in range(0, len(gene_features)):
            sys.stdout.write(str(training_samples[sample_index][feature_index]))
            sys.stdout.write("\t")
        sys.stdout.write("\n")
        sample_index += 1
