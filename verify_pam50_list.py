import data_loader
import pam50

gene_features, samples_names, training_samples = data_loader.loadExpressionData()
pam50_list = pam50.get_pam50_list()

for gene in pam50_list:
    if gene not in gene_features:
        print "Can't find => ", gene, " in our features list"