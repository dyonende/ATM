'''
Authors: Anouk Twilt, Dyon van der Ende, Lois Rink
Argument 1: path to output of baseline classifier
Argument 2: path to output of crf classifier
Argument 3: path to output of svm classifier
Argument 4: path to preprocessed conll data
output: csv files with analysis for each classifier

'''
import sys
import pandas as pd
import os
import collections


baseline_file = sys.argv[1]
crf_file = sys.argv[2]
svm_file = sys.argv[3]
dev_file = sys.argv[4]


def file_to_listrows(filename):
    rows = []
    with open(filename) as infile:
        content= infile.read()
        line = content.split('\n')
        for cells in line:
            rows.append(cells.split('\t'))
    return rows

baseline_rows = file_to_listrows(baseline_file)
svm_rows = file_to_listrows(svm_file)
crf_rows = file_to_listrows(crf_file)
gold_rows = file_to_listrows(dev_file)

def mistakes_dataframe(filename, outfilename):
    counter = 0
    data_list = []
    list_of_lists = []
    feature_dict = dict()
    mistake_counter = 0
    
    if filename == crf_file:
        file_rows = []
        for system, gold in zip(crf_rows, gold_rows):
            system_label = [system[-1]]
            line = gold + system_label
            file_rows.append(line)
    else:
        file_rows = file_to_listrows(filename)
        
            
    for features in file_rows[1:]:
        counter += 1
        if features[13] != features[14]:
            mistake_counter += 1
            feature_dict = {
                'IndexInDataset': counter+1,
                'Token': features[0],
                'lemma': features[1],
                'UPOS': features[2],
                'XPOS': features[3],
                'DepRel': features[4],
                'head': features[5],
                'PrevTok': features[6],
                'PrevPOS': features[7],
                'NextTok': features[8],
                'NextPOS': features[9],
                'NegPrefix': features[10],
                'NegPostfix': features[11],
                'NegExpList': features[12],
                'GoldLabel': features[13],
                'SystemLabel': features[14]
            }
            data_list.append(feature_dict)
        
        if counter >= len(file_rows)-3: # handle empty last line
            break
            
    filename = filename.replace('-out.conll', '')
    mistakes = f'This system ({filename}) made {mistake_counter} mistakes'
    df = pd.DataFrame(data_list)
    df.to_csv(outfilename, sep='\t')
    return data_list, df, mistakes

print(mistakes_dataframe(svm_file, 'svm_stats.csv')[1])
print(mistakes_dataframe(crf_file, 'crf_stats.csv')[1])
print(mistakes_dataframe(baseline_file, 'baseline_stats.csv')[1])

def mistake_counts(filename, statsfile):
    data = mistakes_dataframe(filename, statsfile)[0]
    token_list = []
    lemma_list = []
    UPOS_list = []
    XPOS_list = []
    DepRel_list = []
    head_list = []
    PrevPOS_list = []
    NextPOS_list = []

    for data in data:
        token_list.append(data['Token'])
        lemma_list.append(data['lemma'])
        UPOS_list.append(data['UPOS'])
        XPOS_list.append(data['XPOS'])
        DepRel_list.append(data['DepRel'])
        head_list.append(data['head'])
        PrevPOS_list.append(data['PrevPOS'])
        NextPOS_list.append(data['NextPOS'])
    
    print("-TOKEN-")    
    print(collections.Counter(token_list))
    print('\n\n')
    print("-LEMMA-")
    print(collections.Counter(lemma_list))
    print('\n\n')
    print("-UPOS-")
    print(collections.Counter(UPOS_list))
    print('\n\n')
    print("-XPOS-")
    print(collections.Counter(XPOS_list)) 
    print('\n\n')
    print("-DepRel-")
    print(collections.Counter(DepRel_list))
    print('\n\n')
    print("-head-")
    print(collections.Counter(head_list))
    print('\n\n')
    print("-PrevPos-")
    print(collections.Counter(PrevPOS_list))
    print('\n\n')
    print("-NextPOS-")
    print(collections.Counter(NextPOS_list))
    
    
print(mistake_counts(svm_file, 'svm_stats.csv'))
print(mistake_counts(crf_file, 'crf_stats.csv'))
print(mistake_counts(baseline_file, 'baseline_stats.csv'))
