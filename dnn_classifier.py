import tensorflow as tf
import numpy as np
import data_loader
import sys

tf.logging.set_verbosity(tf.logging.INFO)

gene_features, samples_names, training_samples = data_loader.loadExpressionData()
pam50_by_sample_name = data_loader.load_labels_data(samples_names)
classes = ['Basal', 'Her2', 'LumA', 'LumB', 'Normal']

training_data_by_gene = {}
for gene in gene_features:
    training_data_by_gene[gene] = []

for training_sample in training_samples:
    for i in range(0, len(gene_features)):
        gene = gene_features[i]
        training_data_by_gene.get(gene).append(training_sample[i])

labels = []
for sample_name in samples_names:
    labels.append(pam50_by_sample_name[sample_name])

feature_columns = [tf.contrib.layers.real_valued_column(gene) for gene in gene_features]

# Build 3 layer DNN with 10, 20, 10 units respectively.
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[500],
                                            n_classes=5,
                                            model_dir="/tmp/microarray_dnn_1.0")


# Define the training inputs
def get_train_inputs():
    data_tensor_by_features = {k: tf.constant(training_data_by_gene[k.name], shape=(len(training_samples), 1)) for k in feature_columns}
    y = tf.constant([classes.index(label) for label in labels], shape=(len(training_samples), 1))
    return data_tensor_by_features, y

# Fit model.
classifier.fit(input_fn=get_train_inputs, steps=2000)

ev = classifier.evaluate(input_fn=get_train_inputs, steps=1)

print ev
print "Loss evaluation", ev["loss"]