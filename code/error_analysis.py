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
    """Functions transforms file into a list of lists(rows)"""
    rows = []
    with open(filename) as infile:
        content= infile.read()
        line = content.split('\n')
        for cells in line:
            rows.append(cells.split('\t'))
    return rows

#Transforming all files to lists of rows
baseline_rows = file_to_listrows(baseline_file)
svm_rows = file_to_listrows(svm_file)
crf_rows = file_to_listrows(crf_file)
gold_rows = file_to_listrows(dev_file)
 
    

def mistakes_dataframe(filename, outfilename):
    """Functions takes a file as input and checks if the system label matches the gold label.
    From the mistakes, a dataframe is outputted and saved to a csv-file with the defined outputfilename."""
    counter = 0
    data_list = []
    list_of_lists = []
    feature_dict = dict()
    mistake_counter = 0
    
    #The crf file only makes use of the token and assigns a label. For the mistakes file, we are using the features of the gold file.
    #The features of the gold file are used together with the labels of the crf file to provide the reader with a better understanding of the mistakes.
    if filename == crf_file:
        file_rows = []
        for system, gold in zip(crf_rows, gold_rows):
            system_label = [system[-1]]
            #print(type(system_label))
            #print(gold)
            line = gold + system_label
            file_rows.append(line)
    else: #The baseline and SVM classifier have a file with all the features present, for that reason we just apply the file_to_listrows-function.
        file_rows = file_to_listrows(filename)
        
    #print(len(file_rows))
            
    for features in file_rows[1:]:
        counter += 1
        #To separate FP and FN instances: the following if statement is inserted:
        if features[13] == 'O' and features[14] =='NEG':
            mistake_counter += 1
            #print(features)
            feature_dict = {
                'IndexInDataset': counter+1, #The number from the original dataset is inserted so that the tokens are easy to find.
                'Mistake-type': 'FalsePositive', #All the mistakes are labelled with if they are FP or FN
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
                'SystemLabel': features[14] #This is the label that the system gave to the token
            }
            data_list.append(feature_dict)
           #For the False Negative instances:
        if features[13] == 'NEG' and features[14] =='O':
            mistake_counter += 1
            #print(features)
            feature_dict = {
                'IndexInDataset': counter+1,
                'Mistake-type': 'FalseNegative',
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
        if counter == 13567: #The last line of every classifier is empty, to prevent the code from breaking,this if-statement is inserted.
            break
            

    filename = filename.replace('-out.conll', '')
    mistakes = f'This system ({filename}) made {mistake_counter} mistakes' #The function shows the amount of mistakes the system made
    #print(mistakes)
    df = pd.DataFrame(data_list)
    df.to_csv(outfilename, sep='\t')
    return data_list, df, mistakes #The list of dictionaries, together with the dataframe and the mistakes are returned

#printing the dataframes for all three systems
print(mistakes_dataframe(svm_file, 'svm_new_stats.csv')[1])
print(mistakes_dataframe(crf_file, 'crf_new_stats.csv')[1])
print(mistakes_dataframe(baseline_file, 'baseline_new_stats.csv')[1])


def mistake_counts(filename, statsfile):
    """Function takes the list of dictionaries, generated by the mistakes_dataframe-function and analyzes it in terms of frequency.
    Function prints the mistakes per Mistake-type, POS-type, DepRel-type, head, PreviousPOS and NextPOS.
    Function also prints the amount of False Positives and False Negatives."""

    #The data dat will be used comes from the mistakes_dataframe-function.
    data = mistakes_dataframe(filename, statsfile)[0]

    #For all the types of information, a list will be made, for every false positive and negative, a seperate list will be made.
    fp_token_list = []
    fp_lemma_list = []
    fp_UPOS_list = []
    fp_XPOS_list = []
    fp_DepRel_list = []
    fp_head_list = []
    fp_PrevPOS_list = []
    fp_NextPOS_list = []
    fp_counter = 0 #A counter to count the false positives
    
    fn_token_list = []
    fn_lemma_list = []
    fn_UPOS_list = []
    fn_XPOS_list = []
    fn_DepRel_list = []
    fn_head_list = []
    fn_PrevPOS_list = []
    fn_NextPOS_list = []
    fn_counter = 0 #The false negatives are also counted
    


    for data in data:
        if data['Mistake-type'] == 'FalsePositive': #For all the False Positives, their tokens, lemmas, UPOS-labels, XPOS-Labels, DepRel-labels, heads, PrevPOS-Labels, NextPOS-Labels are appended to separate lists.
            fp_counter += 1
            fp_token_list.append(data['Token'])
            fp_lemma_list.append(data['lemma'])
            fp_UPOS_list.append(data['UPOS'])
            fp_XPOS_list.append(data['XPOS'])
            fp_DepRel_list.append(data['DepRel'])
            fp_head_list.append(data['head'])
            fp_PrevPOS_list.append(data['PrevPOS'])
            fp_NextPOS_list.append(data['NextPOS'])
        
        if data['Mistake-type'] == 'FalseNegative': #The same happens for the False Negatives.
            fn_counter += 1
            fn_token_list.append(data['Token'])
            fn_lemma_list.append(data['lemma'])
            fn_UPOS_list.append(data['UPOS'])
            fn_XPOS_list.append(data['XPOS'])
            fn_DepRel_list.append(data['DepRel'])
            fn_head_list.append(data['head'])
            fn_PrevPOS_list.append(data['PrevPOS'])
            fn_NextPOS_list.append(data['NextPOS'])
    #The mistakes are printed
    print(f"In total, this classifier made {fp_counter} False Positive and {fn_counter} False Negative mistakes")



    #With the help of a counter dictionary, all instances are counted and printed below
    print("-TOKEN-")
    print("FP:")
    print(collections.Counter(fp_token_list))
    print("FN:")
    print(collections.Counter(fn_token_list))
    print('\n\n')
    print("-LEMMA-")
    print("FP:")
    print(collections.Counter(fp_lemma_list))
    print("FN:")
    print(collections.Counter(fn_lemma_list))
    print('\n\n')
    print("-UPOS-")
    print("FP:")
    print(collections.Counter(fp_UPOS_list))
    print("FN:")
    print(collections.Counter(fn_UPOS_list))
    print('\n\n')
    print("-XPOS-")
    print("FP:")
    print(collections.Counter(fp_XPOS_list)) 
    print("FN:")
    print(collections.Counter(fn_XPOS_list))
    print('\n\n')
    print("-DepRel-")
    print("FP:")
    print(collections.Counter(fp_DepRel_list))
    print("FN:")
    print(collections.Counter(fn_DepRel_list))
    print('\n\n')
    print("-head-")
    print("FP:")
    print(collections.Counter(fp_head_list))
    print("FN:")
    print(collections.Counter(fn_head_list))
    print('\n\n')
    print("-PrevPos-")
    print("FP:")
    print(collections.Counter(fp_PrevPOS_list))
    print("FN:")
    print(collections.Counter(fn_PrevPOS_list))
    print('\n\n')
    print("-NextPOS-")
    print("FP:")
    print(collections.Counter(fp_NextPOS_list))
    print("FN:")
    print(collections.Counter(fn_NextPOS_list))

#results for all three systems:
print("------SVM------") 
print(mistake_counts(svm_file, 'svm_new_stats.csv'))
print('\n\n')

print("------CRF------")
print(mistake_counts(crf_file, 'crf_new_stats.csv'))
print('\n\n')

print("------BASELINE------")
print(mistake_counts(baseline_file, 'baseline_new_stats.csv'))