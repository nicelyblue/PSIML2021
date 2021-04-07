from nltk.stem import SnowballStemmer 
from nltk.tokenize import word_tokenize, sent_tokenize
import sys, os, numpy

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def get_file_list(path):
    dirs = os.listdir(path)
    for item in dirs:
        if os.path.isfile(path+'/'+item):
            file_list.append(str(path+'/'+item))
        else:
            get_file_list(path+'/'+item)

def sort_by_order(srt, sent):
    help_dict = {}
    for s in srt:
        help_dict[s] = sent.index(s)
    return sorted(help_dict)

def process_files(file_list):
    stemmed_list = []
    for path in file_list:
        with open(path, encoding='utf-8') as file:
            data = file.read().replace('\n', '')
        terms = word_tokenize(data)
        stemmer = SnowballStemmer("english")
        stemmed = [stemmer.stem(term) for term in terms]
        stemmed_list.append(stemmed)
    return stemmed_list

def score_sentence(sentence, vals):
    score = 0
    terms = word_tokenize(sentence)
    stemmer = SnowballStemmer("english")
    stemmed = [stemmer.stem(term) for term in terms]
    for word in stemmed:
        if word.isalnum():
            try:
                score += vals[word]
            except:
                pass
    return score

def tf(term, terms):
    return terms.count(term)/len(terms)

def idf(term, ind, list_of_texts):
    k_t = 0
    terms = list_of_texts[ind]
    if (term in terms):
        k_t += 1
    return numpy.log(len(file_list)/k_t)

def task_one(ind, list_of_texts):
    tf_idf_dict = {}
    for term in list_of_texts[ind]:
        if term.isalnum():
            term_frequency = tf(term, list_of_texts[ind])
            inverse_document_frequency = idf(term, ind, list_of_texts)
            tf_idf_dict[term] = term_frequency * inverse_document_frequency
    try:
        print(', '.join(sorted(tf_idf_dict)[0:10]))
    except:
        print(', '.join(sorted(tf_idf_dict)))
    return tf_idf_dict

def task_two(tf_idf, file_path):
    sent_score_dict = {}
    with open(file_path, encoding='utf-8') as file:
        data = file.read()
    sentences = sent_tokenize(data)
    for sentence in sentences:
        sent_score_dict[sentence] = score_sentence(sentence, tf_idf)
    try:
        sorted_by_score = sorted(sent_score_dict)[0:5]
    except:
        sorted_by_score = sorted(sent_score_dict)
    sorted_sentences = sort_by_order(sorted_by_score, sentences)
    print(' '.join(sorted_sentences))

corpus_folder = sys.stdin.readline()[:-1]
file_path = sys.stdin.readline()[:-1]
file_list = []
get_file_list(corpus_folder)

list_of_texts = process_files(file_list)
ind = file_list.index(file_path)

tf_idf = task_one(ind, list_of_texts)
task_two(tf_idf, file_path)