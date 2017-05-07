import tensorflow as tf
import numpy as np
import data_loader
import sys

gene_features, samples_names, training_samples = data_loader.loadExpressionData()
pam50_by_sample_name = data_loader.load_labels_data(samples_names)
classes = ['Basal', 'Her2', 'LumA', 'LumB', 'Normal']

labels = []
for sample_name in samples_names:
    labels.append(pam50_by_sample_name[sample_name])

feature_columns = [tf.contrib.layers.real_valued_column(gene) for gene in gene_features]

# Build 3 layer DNN with 10, 20, 10 units respectively.
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[5000, 500, 50],
                                            n_classes=5,
                                            model_dir="/tmp/microarray_dnn_1.0")

# Define the training inputs
def get_train_inputs():
    x = tf.constant(training_samples)
    y = tf.constant([classes.index(label) for label in labels])
    return x, y

# Fit model.
classifier.fit(input_fn=get_train_inputs, steps=2000)