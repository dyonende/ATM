import stanza

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

nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True)

in_data = list()
with open("SEM-2012-SharedTask-CD-SCO-training-simple.txt") as infile:
    data = infile.read().split('\n')
    for line in data[:15000]:
        if len(line) > 0:
            in_data.append(line.split('\t')[:4])
            
chapters = set(in_data[0])
    

sentences = list()
sentence = list()
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

pos_list = list()
lemma_list = list()
for sent in doc.sentences:
    for word in sent.words:
        pos_list.append(word.xpos)
        lemma_list.append(word.lemma)
       

#chapter \t sentence \t token_number \t token \t negation    
prev_token = ""
next_token = ""
prev_pos = ""
next_pos = ""      
        
for i in range(len(in_data)):
    if i > 0:
        prev_token = in_data[i-1][3]
        prev_pos = pos_list[i-1]
    if i+1 < len(in_data):
        next_token = in_data[i+1][3]
        next_pos = pos_list[i+1]
    else:
        next_token = ""
        
    token = in_data[i][3]
    
    print("\t".join(in_data[i]), lemma_list[i], pos_list[i], prev_token, prev_pos, next_token, next_pos, sep='\t')        

     