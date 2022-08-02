from collections import defaultdict as ddict
import sys

#IBM model 2


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

def createAlignment(corpus, t_table, q):
  aligment_file = open("./aligment_IBM2.txt", "w")
  for pair in corpus:
    sentence_align = []
    e_words = pair['en'].strip().split()
    f_words =pair['fr'].strip().split()
    e_len = len(e_words)
    f_len = len(f_words)
    for e_ind, e_word in enumerate(e_words):
      max_pr = 0 
      max_f_index = f_len
      for f_ind, f_word in enumerate(f_words):
        if f_word in t_table[e_word] and  t_table[e_word][f_word]*q[f_ind][e_ind][e_len][f_len] >  max_pr:
          max_pr = t_table[e_word][f_word]*q[f_ind][e_ind][e_len][f_len]
          max_f_index = f_ind
    # Skip words align to null 
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

#Initializing t(e|f) uniformly and q
t_table =ddict(lambda: ddict(lambda: 1/len(english_words)))
q = ddict(lambda: ddict(lambda: ddict(lambda: ddict(lambda: 1/len(english_words)))))

#run until converged
for loop in range(20):
  # train the model
  total_a = ddict(lambda: ddict(lambda: ddict(lambda: 0.0)))
  count_a = ddict(lambda: ddict(lambda: ddict(lambda: ddict(lambda: 0.0))))
  total_e = ddict(float)
  total_f = ddict(float)
  count_ef = ddict(lambda: ddict(float))

# for every sentence in corpus
  for pair in corpus:
    e_words = pair['en'].strip().split()
    f_words =pair['fr'].strip().split()
    e_len = len(e_words)
    f_len = len(f_words)

  # calculate normalization
    for e_ind, e_word in enumerate(e_words):
      total_e[e_word] = 0
      for f_ind, f_word in enumerate(f_words):
        total_e[e_word] += t_table[e_word][f_word] * q[f_ind][e_ind][e_len][f_len]
      #collect counts
      for f_ind, f_word in enumerate(f_words):
        delta = t_table[e_word][f_word] * q[f_ind][e_ind][e_len][f_len] / total_e[e_word]
        count_ef[e_word][f_word] += delta
        total_f[f_word] += delta
        count_a[f_ind][e_ind][e_len][f_len] += delta
        total_a[e_ind][e_len][f_len] += delta


  # set t and q
  english_words, french_words
  for e in t_table.keys():
    for f in t_table[e].keys():
      t_table[e][f] = count_ef[e][f] / total_f[f]

      
  for i in q.keys():
    for j in q[i].keys():
      for e_len in q[i][j].keys():
        for f_len in q[i][j][e_len].keys():
          q[i][j][e_len][f_len] = count_a[i][j][e_len][f_len] / total_a[j][e_len][f_len]
  

# create aligment
createAlignment(corpus, t_table, q)
