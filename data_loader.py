import re
import sys

def loadExpressionData():
    samples_size = 0  # the number of labeled data samples
    samples_names = []
    training_samples = []
    gene_features = []
    with open('BRCA.exp.466.med.txt', 'rb') as expressionDataFile:
        file_line_number = 1
        for data_row in expressionDataFile:
            if file_line_number == 1:
                header_list = re.split(r'\t', data_row.rstrip('\t'))
                samples_size = len(header_list) - 1
                assert samples_size > 1, "number of samples should be greater than one"
                samples_names = [header_list[i] for i in range(1, len(header_list))]
            else:
                if len(training_samples) == 0:
                    for sample_index in range(0, samples_size):
                        training_samples.append([])
                data_list = re.split(r'\t', data_row.rstrip('\t'))
                assert len(data_list) == samples_size + 1, "All data row should have the same dimensions at line number {}".format(file_line_number)
                gene_features.append(data_list[0].strip())
                for sample_index in range(0, samples_size):
                    if data_list[sample_index + 1].strip():
                        value = float(data_list[sample_index + 1].strip())
                    else:
                        value = None
                    training_samples[sample_index].append(value)
            file_line_number += 1
    return (gene_features, samples_names, training_samples)


def load_labels_data(sameples_names):
    expected_labels = set(['Basal', 'Her2', 'LumA', 'LumB', 'Normal'])
    label_by_sample_name_raw = {}
    with open('BRCA.datafreeze.20120227.txt', 'rb') as labelsDataFile:
        file_line_number = 1
        lines = re.split(r'\r', labelsDataFile.readline())
        for data_row in lines:
            if file_line_number > 1:
                data_list = re.split(r'\t', data_row.rstrip('\t\n\r'))
                sample_name = data_list[0].strip()
                pam50_classification_label = data_list[3].strip()
                if pam50_classification_label not in expected_labels:
                    raise TypeError("line {} of BRCA.datafreeze.20120227.txt contains invalid pam50 type={} for sample name={}".format(file_line_number, pam50_classification_label, sample_name))
                label_by_sample_name_raw[sample_name] = pam50_classification_label
            file_line_number += 1

    label_by_sample_name_filtered = {}
    for aliquot_barcode in sameples_names:
        sample_name = convert_aliquot_barcode_to_sample_barcode(aliquot_barcode)
        if sample_name not in label_by_sample_name_raw:
            raise RuntimeError("BRCA.datafreeze.20120227.txt doesn't have a pam50 label for a sample name={}".format(sample_name))
        else:
            label_by_sample_name_filtered[sample_name] = label_by_sample_name_raw[sample_name]

    return label_by_sample_name_filtered


def convert_aliquot_barcode_to_sample_barcode(aliquot_barcode):
    parts = re.split(r'-', aliquot_barcode)
    assert len(parts) == 7
    return "-".join(parts[:4])