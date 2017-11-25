import numpy as np
from gensim.models import Word2Vec
import re, string 
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier

pos_model = Word2Vec.load("final_positive")
neg_model = Word2Vec.load("final_negative")


clean = lambda s: re.sub('['+string.punctuation.replace('+','').replace('/','')+']', '', s)
tokenizer = lambda x: word_tokenize(clean(x.lower()))


def can_be_adjective(word):
    for elem in wn.synsets(word):
        if elem.pos() == 'a':
            return True
    return False




def get_summary(positive_sentences, negative_sentences, num_clusters = 3):

    #Tokenize the sentences
    print("Tokenizing")
    
    pos_token = [tokenizer(i) for i in positive_sentences]
    neg_token = [tokenizer(i) for i in negative_sentences]
    
    #Preparing Vocabulary
    print("Preparing vocabulary")
    
    stop = set(stopwords.words('english'))
    
    vocab = set(pos_model.wv.vocab) - stop
    vocab = [i for i in vocab if can_be_adjective(i)]
    s1 = []
    for sent in pos_token:
        for word in sent:
            if word in vocab:
                s1.append(pos_model[word])
    s1 = np.array(s1)
    
    vocab = set(neg_model.wv.vocab) - stop
    vocab = [i for i in vocab if can_be_adjective(i)]
    s2 = []
    for sent in neg_token:
        for word in sent:
            if word in vocab:
                s2.append(neg_model[word])
    s2 = np.array(s2)
    
    #Clustering
    print("Clustering")
    
    pos_kmeans = KMeans(n_clusters=num_clusters).fit(s1)
    pos_centers = pos_kmeans.cluster_centers_
    pos_neigh = KNeighborsClassifier(n_neighbors=1)
    pos_neigh.fit(s1, pos_kmeans.labels_) 
    neg_kmeans = KMeans(n_clusters=num_clusters).fit(s2)
    neg_centers = neg_kmeans.cluster_centers_
    neg_neigh = KNeighborsClassifier(n_neighbors=1)
    neg_neigh.fit(s2, neg_kmeans.labels_)     
    
    print("Most significant words")
    print("Positives")
    for i in pos_centers:
        print(vocab[pos_neigh.kneighbors(i.reshape(1,-1), return_distance=False)[0,0]])
    print("Negatives")
    for i in neg_centers:
        print(vocab[neg_neigh.kneighbors(i.reshape(1,-1), return_distance=False)[0,0]])



#Example
df = pd.read_csv("Reviews.csv")

ex_product = df[['Text', 'Score']][df['ProductId'] == "B007JFMH8M"]

prod_positives = ex_product['Text'][ex_product['Score'] == 5].as_matrix()
prod_negatives = ex_product['Text'][ex_product['Score'] <= 2].as_matrix()

get_summary(prod_positives, prod_negatives)
