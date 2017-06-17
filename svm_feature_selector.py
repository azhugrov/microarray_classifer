import math

def select_genes(coefficients, gene_features):
    selected_genes = dict()
    top_features_by_classifier = [[] for c in coefficients]
    # for every classifier select top 50 genes
    for classifier_index in range(0, len(coefficients)):
        class_coefficients = coefficients[classifier_index]
        # coefficient for a single classifier
        squares_with_feature_index = []
        for i in range(0, len(class_coefficients)):
            module = math.fabs(class_coefficients[i])
            squares_with_feature_index.append((module, i))
        # sort in desc order to select most important features
        sorted_desc = sorted(squares_with_feature_index, key=lambda f: f[0], reverse=True)
        for i in range(0, 50):
            top_feature = sorted_desc[i]
            top_features_by_classifier[classifier_index].append((top_feature[0], top_feature[1], gene_features[top_feature[1]]))

    for top_features in top_features_by_classifier:
        for top_feature in top_features:
            if top_feature[2] not in selected_genes:
                selected_genes[top_feature[2]] = (top_feature[1], top_feature[2])

    for key, value in selected_genes.iteritems():
        print key, value[0]

    selected_matrix = []
    for i in range(0, len(gene_features)):
        if gene_features[i] in selected_genes:
            selected_matrix.append(True)
        else:
            selected_matrix.append(False)

    return selected_matrix