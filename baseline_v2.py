# baseline 
with open('dev_preprocessed.conll', 'r') as infile:
    data = infile.read().split('\n')
    for line in data:
        columns = line.split('\t')
        neg_list = list()
        try:
            if columns[10] == 'True' or columns[11] == 'True' or columns[12] == 'True':
                print(line + '\t' + 'NEG')
            else:
                print(line + '\t' + 'O')
        except KeyboardInterrupt:
            break;
        except:
            print(line)
