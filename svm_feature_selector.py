import math

def select_genes(coefficients, classes_ordered, gene_features, pam50_genes):
    selected_genes = dict()
    top_features_by_classifier = [[] for c in coefficients]
    # for every classifier select top 50 genes
    for classifier_index in range(0, len(coefficients)):
        class_coefficients = coefficients[classifier_index]
        # coefficient for a single classifier
        module_with_feature_index = []
        for i in range(0, len(class_coefficients)):
            module = math.fabs(class_coefficients[i])
            module_with_feature_index.append((module, i))
        # sort in desc order to select most important features
        sorted_desc = sorted(module_with_feature_index, key=lambda f: f[0], reverse=True)
        for i in range(0, len(sorted_desc)):
            top_feature = sorted_desc[i]
            if top_feature[0] > 0:
                top_features_by_classifier[classifier_index].append((top_feature[0], top_feature[1], gene_features[top_feature[1]]))

        print "Top features for classifier {}:".format(classes_ordered[classifier_index])
        order_index = 1
        for top_feature_with_label in top_features_by_classifier[classifier_index]:
            gene_label = top_feature_with_label[2]
            if gene_label in pam50_genes:
                print "   {}. Gene: \"{}\" has score: \"{}\" IsPam50".format(order_index, gene_label, top_feature_with_label[0])
            else:
                print "   {}. Gene: \"{}\" has score: \"{}\"".format(order_index, gene_label, top_feature_with_label[0])
            order_index += 1
        print ""
        print ""
        print ""
        print ""
        print ""

    for top_features_per_classifier in top_features_by_classifier:
        selected_genes_number = len(top_features_per_classifier)
        if selected_genes_number > 50:
            for index in range(0, 50):
                top_feature = top_features_per_classifier[index]
                if top_feature[2] not in selected_genes:
                    selected_genes[top_feature[2]] = (top_feature[1], top_feature[2])
        else:
            for top_feature in top_features_per_classifier:
                if top_feature[2] not in selected_genes:
                    selected_genes[top_feature[2]] = (top_feature[1], top_feature[2])

    # for key, value in selected_genes.iteritems():
    #     print key, value[0]

    selected_matrix = []
    for i in range(0, len(gene_features)):
        if gene_features[i] in selected_genes and gene_features[i] not in pam50_genes:
            selected_matrix.append(True)
        else:
            selected_matrix.append(False)

    return selected_matrix