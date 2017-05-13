import tensorflow as tf
import numpy as np
import data_loader
import sys
from sklearn.model_selection import train_test_split

tf.logging.set_verbosity(tf.logging.INFO)

gene_features, samples_names, expression_samples = data_loader.loadExpressionData()
pam50_by_sample_name = data_loader.load_labels_data(samples_names)
classes = ['Basal', 'Her2', 'LumA', 'LumB', 'Normal']
pam50_labels = []
for sample_name in samples_names:
    pam50_labels.append(pam50_by_sample_name[sample_name])

training_expression_samples, test_expression_samples, training_pam50_labels, test_pam50_labels = train_test_split(expression_samples, pam50_labels, test_size=0.2, random_state=0)

feature_columns = [tf.contrib.layers.real_valued_column(gene) for gene in gene_features]

# Build 3 layer DNN with 10, 20, 10 units respectively.
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[500],
                                            n_classes=5,
                                            model_dir="/tmp/microarray_dnn_1.0")

# Define the training inputs
def get_inputs(expression_samples, pam50Labels):
    expression_data_by_gene = {}
    for gene in gene_features:
        expression_data_by_gene[gene] = []

    for sample in expression_samples:
        for i in range(0, len(gene_features)):
            gene = gene_features[i]
            expression_data_by_gene.get(gene).append(sample[i])

    data_tensor_by_features = {k: tf.constant(expression_data_by_gene[k.name], shape=(len(expression_samples), 1)) for k in feature_columns}
    y = tf.constant([classes.index(label) for label in pam50Labels], shape=(len(expression_samples), 1))
    return data_tensor_by_features, y

# Fit model.
classifier.fit(input_fn=lambda: get_inputs(training_expression_samples, training_pam50_labels), steps=2000)
ev = classifier.evaluate(input_fn=lambda: get_inputs(test_expression_samples, test_pam50_labels), steps=1)

print ev
print "Loss evaluation", ev["loss"]