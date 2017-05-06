import data_loader
from sklearn import svm
from sklearn.model_selection import cross_val_score

gene_features, samples_names, training_samples = data_loader.loadExpressionData()
pam50_by_sample_name = data_loader.load_labels_data(samples_names)

labels = []
for sample_name in samples_names:
    labels.append(pam50_by_sample_name[sample_name])

clf = svm.SVC(kernel='sigmoid', C=1)
scores = cross_val_score(clf, training_samples, labels, cv=5)

print "scores: ", scores