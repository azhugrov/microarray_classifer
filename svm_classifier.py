from sklearn import svm
import numpy
import data_loader
import sys

gene_features, samples_names, training_samples = data_loader.loadExpressionData()
pam50_by_sample_name = data_loader.load_labels_data(samples_names)

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

X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC()
clf.fit(X, y)

