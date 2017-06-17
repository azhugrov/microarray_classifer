import data_loader
import pam50
from sklearn import svm
from sklearn.model_selection import cross_val_score
import svm_feature_selector as fs

gene_features, samples_names, training_samples = data_loader.loadExpressionData()
target_label_by_sample_name = data_loader.load_labels_data(samples_names)
pam50_genes = pam50.get_pam50_list()

labels = []
for sample_name in samples_names:
    labels.append(target_label_by_sample_name[sample_name])

clf = svm.LinearSVC(penalty='l1', C=1, dual=False)
clf.fit(training_samples, labels)
coefficients = clf.coef_
classes_ordered = clf.classes_
# investigate the final matrix
selected_genes = fs.select_genes(coefficients, classes_ordered, gene_features, pam50_genes)

training_samples_reduced = []
for sample in training_samples:
    training_samples_reduced.append([sample[i] for i in range(0, len(sample)) if selected_genes[i]])

scores = cross_val_score(clf, training_samples_reduced, labels, cv=5)

# clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(5000, 1000), random_state=1, verbose=True)
# scores = cross_val_score(clf, training_samples, labels, cv=5)
print "scores: ", scores