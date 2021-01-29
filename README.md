# Negation Cue Detection
Authors: Anouk Twilt, Dyon van der Ende, Lois Rink

## Requirements
the following Python 3.8.5 modules are required to run the scripts:
- pandas 1.1.5
- sys
- os
- collections
- sklearn 0.0
- csv 
- sklearn_crfsuite 0.3.6
- stanza 1.1.1 (with processors tokenize, pos, lemma and depparse from the ewt package)

## Files
These files are designed to work with the SEM-2012-SharedTask-CD-SCO data.
It is advised to run them in order of appearance below.

- code/preprocess.py
this file preprocesses a conll file for use with the scripts mentioned below.
The pre-processed data is printed to the terminal. Bash redirect ('>') can be
used to save it.
Argument 1: conll file
output: pre-processed data printed to terminal

- code/data_stats.py
extracts some basic descriptive statistics of the data set.
Argument 1: path to conll data set
Output: statistics on data are printed to the terminal

- code/baseline.py
A simple rule-based baseline that works with pre-processed conll files.
The predictions are printed to the terminal. Bash redirect ('>') can be
used to save it.
Argument 1: pre-processed conll file
Output: predictions printed to the terminal

- code/svm.py
A SVM classifier that works with the pre-processed conll files.
Argument 1: pre-processed train file in conll format
Argument 2: pre-processed test file in conll format
Argument 3: output file
Output: the predictions of the classifier are saved to the specified location

- code/crf.py
A CRF classifier that works with the pre-processed conll files.
Argument 1: Pre-processed training data in conll format
Argument 2: pre-processed test data in conll format
Argument 3: output file
Output: the predictions of the classifier are saved to the specified location


- code/evaluate.py
Provides an overview of the metrics and the confusion matrix for the output of 
all classifiers at once. Output is printed to the terminal.
Argument 1: output of baseline classifier
Argument 2: output of SVM classifier
Argument 3: output of CRF classifier
Output: evaluation metrics printed to the terminal

- code/error_analysis.py
outputs a csv file with statistics on the errors that classifiers made.
Argument 1: path to output of baseline classifier
Argument 2: path to output of crf classifier
Argument 3: path to output of svm classifier
Argument 4: path to preprocessed conll data
output: csv files with analysis for each classifier
