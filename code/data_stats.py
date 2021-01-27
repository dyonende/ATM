'''
Authors: Anouk Twilt, Dyon van der Ende, Lois Rink
Argument 1: path to conll data set
'''
import sys
import pandas as pd
import os
import collections


def file_to_listrows(filepath):
    rows = []
    with open(filepath) as infile:
        content= infile.read()
        line = content.split('\n')
        for cells in line:
            rows.append(cells.split('\t'))
    return rows

def data_stats(filepath):
    counter = 0
    token_list = []
    lemma_list = []
    UPOS_list = []
    XPOS_list = []
    DepRel_list = []
    head_list = []
    PrevPOS_list = []
    NextPOS_list = []
    rows = file_to_listrows(filepath)

    for row in rows:
        counter += 1
        token_list.append(row[0])
        lemma_list.append(row[1])
        UPOS_list.append(row[2])
        XPOS_list.append(row[3])
        DepRel_list.append(row[4])
        head_list.append(row[5])
        PrevPOS_list.append(row[7])
        NextPOS_list.append(row[9])
        if counter >= len(rows)-1:  #handle last line that is empty
            break
            
    print("-TOKEN-")           
    print(f"There are {len(set(token_list))} different tokens present in this dataset")
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
    print("-PrevPos-")
    print(collections.Counter(PrevPOS_list))
    print('\n\n')
    print("-NextPOS-")
    print(collections.Counter(NextPOS_list))
    

data_stats(sys.argv[1])