import data_loader
import pickle

from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import ExtraTreesClassifier

gene_features, samples_names, training_samples = data_loader.loadExpressionData()
pam50_by_sample_name = data_loader.load_labels_data(samples_names)

labels = []
for sample_name in samples_names:
    labels.append(pam50_by_sample_name[sample_name])

selected_features = [True for i in range(0, len(gene_features))]

# We use the base estimator LassoCV since the L1 norm promotes sparsity of features.
clf = ExtraTreesClassifier()
clf.fit(training_samples, labels)
print "feature importancies", clf.feature_importances_

sfm = SelectFromModel(clf, prefit=True, threshold=0.001)
n_features = sfm.transform(training_samples).shape[1]

# Reset the threshold till the number of features equals two.
# Note that the attribute can be set directly instead of repeatedly
# fitting the metatransformer.
while n_features > 100:
    sfm.threshold = sfm.threshold * 1.5
    X_transform = sfm.transform(training_samples)
    n_features = X_transform.shape[1]
    selected_features = sfm.get_support(False)

pickle.dump(selected_features, open('selected_features_array.pkl', 'wb'))
print "Finished the model selection to {} genes.".format(n_features)
