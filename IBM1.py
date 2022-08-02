
from collections import defaultdict as ddict
import numpy as np
import sys

#create corpus list
'''
corpus = [{'en': 'each of them is very complex... ',
             'fr': 'chacun en lui - même est très complexe et le lien entre...'}]
'''
def createCorpus(e_file, f_file):
    corpus=[]
    english_data = open(e_file, 'r')
    french_data = open(f_file, 'r')

    english_lines = english_data.read().splitlines() 
    french_lines = french_data.read().splitlines() 
    # insert to the list dict object of the sentences
    for i, e_line in enumerate(english_lines):
        corpus.append({'en': e_line, 'fr':french_lines[i] })
    return corpus

def createUniqueWordsList(corpus, language):
    unique_words = []
    corpus_len = len(corpus)
    for index in range(corpus_len):
        sentence = corpus[index][language].strip().split()
        for word in sentence:
            if word not in unique_words:
                unique_words.append(word)
    return unique_words

def train(corpus,t_table):
    ec_n = ddict(lambda: 0) 
    ec_d = ddict(lambda: 0) 
    # for every sentence in corpus
    for pair in corpus:
      e_words = pair['en'].strip().split()
      f_words =pair['fr'].strip().split()
      e_len = len(e_words)
      f_len = len(f_words)

      for j in range(e_len):
        arr = np.zeros(f_len)
        for i in range(f_len):
          arr[i]=t_table[e_words[j],f_words[i]]
        arr = arr/np.sum(arr)
        #collect counts
        for i in range(f_len):
            ec_n[e_words[j],f_words[i]] += arr[i]
            ec_d[f_words[i]]+=arr[i]
    # estimiate propabilites
    for ej,fi in t_table.keys():
      # calculate p(fj|ei) table from expected counts
      t_table[ej,fi] = ec_n[ej,fi]/ec_d[fi]
    return t_table

def createAlignment(corpus, t_table):
  aligment_file = open("./aligment_IBM1.txt", "w")
  for pair in corpus:
    sentence_align = []
    e_words = pair['en'].strip().split()
    f_words =pair['fr'].strip().split()
    f_len = len(f_words)
    for e_ind, e_word in enumerate(e_words):
      max_pr = 0 
      max_f_index = f_len
      for f_ind, f_word in enumerate(f_words):
        if (e_word,f_word) in t_table and t_table[e_word,f_word] >  max_pr:
          max_pr = t_table[e_word,f_word]
          max_f_index = f_ind
      if( max_f_index != f_len):    
        sentence_align.append(str(max_f_index)+'-'+str(e_ind))
    aligment_file.write(' '.join(sentence_align) +'\n')
  aligment_file.close()

#get files from command line
e_file = sys.argv[1]
f_file = sys.argv[2]

# initilaize corpus
corpus = createCorpus(e_file, f_file)
# create lists of words in english and in french(only one instance of every word)
english_words = createUniqueWordsList(corpus, 'en')
french_words = createUniqueWordsList(corpus, 'fr')

#Initializing t(e|f) uniformly
t_table = ddict(lambda: 1/len(english_words))

#run until converged
for loop in range(20):
  # train the model
  t_table = train(corpus, t_table)

# round t_table
for k, v in t_table.items():
  t_table[k] = round(v, 3)


t_file = open("./t_IBM1.txt", "w")
t_file.write(str(t_table) )
t_file.close()
# create aligment
createAlignment(corpus, t_table)


