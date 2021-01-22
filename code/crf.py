'''
Authors: Anouk Twilt, Dyon van der Ende, Lois Rink
Argument 1: Pre-processed training data in conll format
Argument 2: pre-processed test data in conll format
Argument 3: output file
'''
import sklearn
import sys
import csv
import sklearn_crfsuite
from sklearn_crfsuite import metrics



## based on https://github.com/cltl/ba-text-mining/blob/master/lab_sessions/lab4/Lab4a.4-NERC-CRF-Dutch.ipynb


def token2features(sentence, i):

    token = sentence[i][0]
    lemma = sentence[i][1]
    upos = sentence[i][2]
    xpos = sentence[i][3]
    DepRel = sentence[i][4]
    head = sentence[i][5]
    PrevTok = sentence[i][6]
    PrevPOS = sentence[i][7]
    NextTok = sentence[i][8]
    NextPOS = sentence[i][9]
    NegPrefix = sentence[i][10]
    NegPostfix = sentence[i][11]
    NegExpList = sentence[i][12]
    GoldLabel = sentence[i][13]
    
    features = {
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
    return features

def sent2features(sent):
    return [token2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    #if you added features to your input file, make sure to add them here as well.
    return [Label for Token,Lemma,UPOS,XPOS,DepRel,Head,PrevToken,PrevPOS,NextToken,NextPOS,NegPrefix,NegPostfix,NegExpList, Label  in sent]

def sent2tokens(sent):
    return [Token for Token,Lemma,UPOS,XPOS,DepRel,Head,PrevToken,PrevPOS,NextToken,NextPOS,NegPrefix,NegPostfix,NegExpList, Label  in sent]
    
    
def extract_sents_from_conll(inputfile):
    
    csvinput = open(inputfile,'r')
    csvreader = csv.reader(csvinput,delimiter='\t')
    sents = []
    current_sent = []
    for row in csvreader:
        current_sent.append(tuple(row))
        #note that this is a simplification that works well for this particular data, in other situations, you may need to do more advanced preprocessing to identify sentence boundaries
        if row[0] == ".":
            sents.append(current_sent)
            current_sent = []
    if current_sent != []:
        sents.append(current_sent)
    return sents


def train_crf_model(X_train, y_train):

    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)
    
    return crf

def create_crf_model(trainingfile):

    train_sents = extract_sents_from_conll(trainingfile)
    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]

    crf = train_crf_model(X_train, y_train)
    
    return crf


def run_crf_model(crf, evaluationfile):

    test_sents = extract_sents_from_conll(evaluationfile)
    X_test = [sent2features(s) for s in test_sents]
    y_pred = crf.predict(X_test)
    
    return y_pred, X_test

def write_out_evaluation(eval_data, pred_labels, outputfile):

    outfile = open(outputfile, 'w')
    
    for evalsents, predsents in zip(eval_data, pred_labels):
        for data, pred in zip(evalsents, predsents):
            outfile.write(data.get('token') + "\t" + pred + "\n")

def train_and_run_crf_model(trainingfile, evaluationfile, outputfile):

    crf = create_crf_model(trainingfile)
    pred_labels, eval_data = run_crf_model(crf, evaluationfile)
    write_out_evaluation(eval_data, pred_labels, outputfile)

def main(argv=None):

    if argv is None:
        argv = sys.argv
        
    trainingfile = argv[1]
    evaluationfile = argv[2]
    outputfile = argv[3]
    
    train_and_run_crf_model(trainingfile, evaluationfile, outputfile)


if __name__ == '__main__':
    main()
