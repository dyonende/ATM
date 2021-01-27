# Negation Cue Detection
Authors: Anouk Twilt, Dyon van der Ende, Lois Rink


These files are designed to work with the SEM-2012-SharedTask-CD-SCO data.

- code/preprocess.py
this file preprocesses a conll file for use with the scripts mentioned below.

- code/baseline.py
A simple rule-based baseline that works with pre-processed conll files.

- code/svm.py
A SVM classifier that works with the pre-processed conll files.

- code/crf.py
A CRF classifier that works with the pre-processed conll files.

- code/evaluate.py
Provides an overview of the metrics and the confusion matrix for the output of all classifiers at once.

- code/data_stats.py
extracts some basic descriptive statistics of the data set.

- code/error_analysis.py
outputs a csv file with statistics on the errors that classifiers made.
