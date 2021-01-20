from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import recall_score
import pandas as pd

svm_data = pd.read_csv("out.conll", sep='\t', header=0)
baseline_data = pd.read_csv("base_out.conll", sep='\t', header=0)
gold = svm_data["Label"]
svm_labels = svm_data["Label.1"]
baseline_labels = baseline_data["O"]

print("----SVM----")
print(precision_recall_fscore_support(gold, svm_labels, average='macro'))
print(confusion_matrix(gold, svm_labels))

print("\n----baseline----")
print(precision_recall_fscore_support(gold, baseline_labels, average='macro'))
print(confusion_matrix(gold, baseline_labels))