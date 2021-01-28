'''
Authors: Anouk Twilt, Dyon van der Ende, Lois Rink
Argument 1: conll file
'''
import stanza
import sys

inputfile = sys.argv[1]
Heading = True

#negation cues according to NegExpList
adverbs = {"never", "not", "not"}
prefix_adjective = {"im", "in", "ir", "un"}
suffix_adjective = {"less"}
suffix_verb = {"not", "n't"}
prefix_verb = {"un"}
determiners = {"no"}
interjection = {"no"}
pronouns = {"nothing"}
prepositions = {"without"}
verbs = {"fail"}

def read_file():
    '''
    read in conll file to list of list
    '''
    in_data = list()
    with open(inputfile) as infile:
        data = infile.read().split('\n')
        for line in data:
            if len(line) > 0: #skip empty lines
                in_data.append(line.split('\t'))
    
    return in_data
    
def tokens_to_list(data):
    '''
    prepare all sentences as list of tokens for Stanza to process   
    '''
    sentence = list()   #used for the current sentence
    sentences = list()  #contains all sentences
    for line in data:
        if line[2] == '0':  #first token of sentence
            sentences.append(sentence)
            sentence= list()
            sentence.append(line[3])
        elif int(line[2]) > 0:
            sentence.append(line[3])
      
    sentences.append(sentence)  
    sentences = sentences[1:]   #first entry is empty because of implementation
    return sentences
    
def extract_and_print(doc, data):
    '''
    extract all the features and print to terminal
    '''
    #extract features from processed data
    xpos_list = list()
    upos_list = list()
    lemma_list = list()
    deprel_list = list()
    head_list = list()
    
    for sent in doc.sentences:
        for word in sent.words:
            xpos_list.append(word.xpos)
            upos_list.append(word.upos)
            lemma_list.append(word.lemma)
            deprel_list.append(word.deprel)
            head_list.append(sent.words[word.head-1].text)
            
    #print column names
    if Heading:
        print("Token\tLemma\tUPOS\tXPOS\tDepRel\tHead\tPrevToken\tPrevPOS\tNextToken\tNextPOS\tNegPrefix\tNegPostfix\tNegExpList\tLabel")
           
    #initialise empty for first line
    prev_token = ""
    next_token = ""
    prev_pos = ""
    next_pos = ""      
    for i in range(len(data)):
        #handle first and last line
        if i > 0:
            prev_token = data[i-1][3]
            prev_pos = xpos_list[i-1]
        if i+1 < len(data):
            next_token = data[i+1][3]
            next_pos = xpos_list[i+1]
        else:
            next_token = ""
            next_pos = ""
            
        token = data[i][3]
        
        negation_prefix = False 
        negation_postfix = False
        in_NegExpList = False
        
        #apply NegExpList    
        if upos_list[i]=="ADV" and lemma_list[i] in adverbs:
            in_NegExpList = True
        elif upos_list[i]=="DET" and lemma_list[i] in determiners:
            in_NegExpList = True
        elif upos_list[i]=="VERB" and lemma_list[i] in verbs:
            in_NegExpList = True
        elif upos_list[i]=="INTJ" and lemma_list[i] in interjection:
            in_NegExpList = True
        elif upos_list[i]=="PRON" and lemma_list[i] in pronouns:
            in_NegExpList = True
        elif xpos_list[i]=="IN" and lemma_list[i] in prepositions:
            in_NegExpList = True
            
        if upos_list[i]=="ADJ":
            for prefix in prefix_adjective:
                if token.startswith(prefix):
                    negation_prefix = True
            for suffix in suffix_adjective:
                if token.endswith(suffix):
                    negation_postfix = True
        elif upos_list[i]=="VERB":
            for prefix in prefix_verb:
                if token.startswith(prefix):
                    negation_prefix = True
            for suffix in suffix_verb:
                if token.endswith(suffix):
                    negation_postfix = True
           
        #strip B and I from label B-NEG --> NEG
        gold = data[i][4]
        if gold != "O":
            gold = "NEG"
        
        #output to terminal in conll format
        print(token, lemma_list[i], upos_list[i], xpos_list[i], deprel_list[i], head_list[i], prev_token, prev_pos, next_token, next_pos, negation_prefix, negation_postfix, in_NegExpList, gold, sep='\t')  
         
    

def main():
    #loading nlp pipeline
    nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse', tokenize_pretokenized=True)

    data = read_file() 
    
    #process sentences with stanza 
    doc = nlp(tokens_to_list(data))
    
    extract_and_print(doc, data)
    
if __name__ == "__main__":
    main()     