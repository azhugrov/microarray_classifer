import data_loader
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
import svm_feature_selector as fs

gene_features, samples_names, training_samples = data_loader.loadExpressionData()
pam50_by_sample_name = data_loader.load_labels_data(samples_names)

labels = []
for sample_name in samples_names:
    labels.append(pam50_by_sample_name[sample_name])

clf = svm.LinearSVC(penalty='l1', C=1, dual=False)
clf.fit(training_samples, labels)
coefficients = clf.coef_
# investigate the final matrix
selected_genes = fs.select_genes(coefficients, gene_features)

training_samples_reduced = []
for sample in training_samples:
    training_samples_reduced.append([sample[i] for i in range(0, len(sample)) if selected_genes[i]])

scores = cross_val_score(clf, training_samples_reduced, labels, cv=5)

# clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(5000, 1000), random_state=1, verbose=True)
# scores = cross_val_score(clf, training_samples, labels, cv=5)
print "scores: ", scores