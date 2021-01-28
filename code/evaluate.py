'''
Authors: Anouk Twilt, Dyon van der Ende, Lois Rink
Argument 1: output of baseline classifier
Argument 2: output of SVM classifier
Argument 3: output of CRF classifier
'''
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import recall_score
import pandas as pd
import sys

def main():
    baseline_file = sys.argv[1]
    svm_file = sys.argv[2]
    crf_file = sys.argv[3]

    svm_data = pd.read_csv(svm_file, sep='\t', header=0)
    baseline_data = pd.read_csv(baseline_file, sep='\t', header=0)
    crf_data = pd.read_csv(crf_file, sep='\t', header=0)
    gold = svm_data["Label"]
    svm_labels = svm_data["Label.1"]
    baseline_labels = baseline_data["O"]
    crf_labels = crf_data["Label"]


    print(f"----SVM----")
    print(precision_recall_fscore_support(gold, svm_labels, average='macro'))
    print(confusion_matrix(gold, svm_labels))

    print(f"\n----baseline----")
    print(precision_recall_fscore_support(gold, baseline_labels, average='macro'))
    print(confusion_matrix(gold, baseline_labels))

    print(f"\n----crf----")
    print(precision_recall_fscore_support(gold, crf_labels, average='macro'))
    print(confusion_matrix(gold, crf_labels))

    
if __name__ == "__main__":
    main()