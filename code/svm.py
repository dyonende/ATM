'''
Authors: Anouk Twilt, Dyon van der Ende, Lois Rink
Argument 1: pre-processed train file in conll format
Argument 2: pre-processed test file in conll format
Argument 3: output file

Based on https://github.com/cltl/ma-ml4nlp-labs/blob/main/code/assignment1/basic_system.ipynb
'''
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
import sys

inputfile = sys.argv[1]
devfile = sys.argv[2]
outfile = sys.argv[3]

def extract_features(inputfile):
    """Function extracts features from inputfile and returns them in a list of dicts"""
    data = []   #features
    gold = []   #gold labels

    with open(inputfile, 'r', encoding='utf8') as infile:
        for line in infile:
            components = line.rstrip('\n').split('\t')
            if len(line) > 0:
                token = components[0]
                lemma = components[1]
                upos = components[2]
                xpos = components[3]
                DepRel = components[4]
                head = components[5]
                PrevTok = components[6]
                PrevPOS = components[7]
                NextTok = components[8]
                NextPOS = components[9]
                NegPrefix = components[10]
                NegPostfix = components[11]
                NegExpList = components[12]
                GoldLabel = components[13]


                feature_dict = {
                    'token': token,
                    'lemma': lemma,
                    'UPOS': upos,
                    'XPOS': xpos,
                    'DepRel': DepRel,
                    'head': head,
                    'PrevTok': PrevTok,
                    'PrevPOS': PrevPOS,
                    'NextTok': NextTok,
                    'NextPOS': NextPOS,
                    'NegPrefix': NegPrefix,
                    'NegPostfix': NegPostfix,
                    'NegExpList': NegExpList
                }

            data.append(feature_dict)
            gold.append(GoldLabel)

    return data, gold


def create_classifier(train_features, train_targets, modelname):
    """Function creates and trains a classifier based on a set of training features and gold labels to the trainingdata, classifier can ben specified."""
    if modelname == 'SVM':
        model = svm.LinearSVC(max_iter=10000)

    vec = DictVectorizer()
    features_vectorized = vec.fit_transform(train_features)
    model.fit(features_vectorized, train_targets)

    return model, vec


def classify_data(model, vec, inputfile, outputfile):
    """classifies new data with the previously created classifier"""

    features, gold = extract_features(inputfile)
    features = vec.transform(features)
    predictions = model.predict(features)
    outfile = open(outputfile, 'w')
    counter = 0
    for line in open(inputfile, 'r'):
        if len(line.rstrip('\n').split()) > 0:
            outfile.write(line.rstrip('\n') + '\t' + predictions[counter] + '\n')
            counter += 1
    outfile.close()


def main():
    features, gold = extract_features(inputfile)
    model, vec = create_classifier(features, gold, 'SVM')
    classify_data(model, vec, devfile, outfile)

main()

