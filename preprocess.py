import stanza

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

nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse', tokenize_pretokenized=True)

in_data = list()
token_list = list()
with open("SEM-2012-SharedTask-CD-SCO-training-simple.txt") as infile:
    data = infile.read().split('\n')
    for line in data:
        if len(line) > 0: #skip empty lines
            in_data.append(line.split('\t')[:4])
            token_list.append(line.split('\t')[3])
                

sentences = list()
sentence = list()
#list of sentences for stanza to process
for line in in_data:
    if line[2] == '0':
        sentences.append(sentence)
        sentence= list()
        sentence.append(line[3])
    elif int(line[2]) > 0:
        sentence.append(line[3])
  
sentences.append(sentence)  
sentences = sentences[1:]
        
doc = nlp(sentences)

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
        
       
#initialise empty for first line
prev_token = ""
next_token = ""
prev_pos = ""
next_pos = ""      
        
for i in range(len(in_data)):
    #handle first and last line
    if i > 0:
        prev_token = in_data[i-1][3]
        prev_pos = xpos_list[i-1]
    if i+1 < len(in_data):
        next_token = in_data[i+1][3]
        next_pos = xpos_list[i+1]
    else:
        next_token = ""
        next_pos = ""
        
    token = in_data[i][3]
    
    negation_prefix = False 
    negation_postfix = False
    in_NegExpList = False
    
    #scan for negation cues    
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
    
    #output to terminal in conll format
    print(token_list[i], lemma_list[i], upos_list[i], xpos_list[i], deprel_list[i], head_list[i], prev_token, prev_pos, next_token, next_pos, negation_prefix, negation_postfix, in_NegExpList, sep='\t')  
     