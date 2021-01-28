'''
Authors: Anouk Twilt, Dyon van der Ende, Lois Rink
Argument 1: pre-processed conll file
'''
import sys

def run_classifier():
    '''
    labels the input token with NEG or O and prints to terminal
    '''
    with open(sys.argv[1], 'r') as infile:
        data = infile.read().split('\n')
        for line in data:
            columns = line.split('\t')
            try:
                #if one of the columns NegPrefix, NegPostfix or NegExpList is true, predict NEG
                if columns[10] == 'True' or columns[11] == 'True' or columns[12] == 'True':
                    print(line + '\t' + 'NEG')
                else:
                    print(line + '\t' + 'O')
            except KeyboardInterrupt:
                break;
            except:
                sys.stderr.write(f"found corrupt entry:\t {line}")
            
if __name__ == "__main__":
    run_classifier()
