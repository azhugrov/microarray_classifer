from sklearn import svm
import numpy
import data_loader
import sys

gene_features, samples_names, training_samples = data_loader.loadExpressionData()
pam50_by_sample_name = data_loader.load_labels_data(samples_names)

labels = []
for sample_name in samples_names:
    labels.append(pam50_by_sample_name[sample_name])

clf = svm.SVC()
clf.fit(training_samples, labels)