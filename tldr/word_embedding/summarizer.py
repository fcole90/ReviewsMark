import numpy as np
from gensim.models import Word2Vec
import re, string 
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import os
import time
import pandas as pd
import scipy as sp
import scipy.spatial
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier

THIS_FILE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))
NLTK_SAVE_DIR = os.path.join(os.path.join(THIS_FILE_FOLDER, "NLTK"))
MODELS_DIR = os.path.join(os.path.join(THIS_FILE_FOLDER, "models"))

positive_model = Word2Vec.load(os.path.join(MODELS_DIR, "final_positive.pickle"))
negative_model = Word2Vec.load(os.path.join(MODELS_DIR, "final_negative.pickle"))


clean = lambda s: re.sub('['+string.punctuation.replace('+','').replace('/','')+']', '', s)
tokenizer = lambda x: word_tokenize(clean(x.lower()))


def can_be_adjective(word):
    for elem in wn.synsets(word):
        if elem.pos() == 'a':
            return True
    return False

def cluster_word_dict(idx, model):
    return dict(zip(model.wv.index2word, idx))

def make_clusters(word_vectors, clusters_amount=3):
    start = time.time()  # Start time

    num_clusters = clusters_amount

    # Initalize a k-means object and use it to extract centroids
    kmeans_clustering = KMeans(n_clusters=num_clusters, n_jobs=-1)
    idx = kmeans_clustering.fit_predict(word_vectors)

    # Get the end time and print how long the process took
    end = time.time()
    elapsed = end - start
    print("Time taken for K Means clustering: " + str(elapsed) + "seconds.")

    return kmeans_clustering.cluster_centers_


def print_clusters_centroids_to_words(kmeans_clusters_centroids, vocabulary, model):

    min_words_list = list()
    for centroid in kmeans_clusters_centroids:
        min = np.inf
        min_w = "None"
        for word in vocabulary:
            dist = sp.spatial.distance.cosine(centroid, model[word])
            if dist < min:
                min = dist
                min_w = word
        print(min_w)
        min_words_list.append(min_w)
    return min_words_list


def get_summary(positive_sentences, negative_sentences, num_clusters=3):
    # Tokenize the sentences
    print("Tokenizing")

    positive_tokens = [tokenizer(sentence) for sentence in positive_sentences]
    negative_token = [tokenizer(sentence) for sentence in negative_sentences]
    print("Positive tokens: {}".format(positive_tokens))

    # Preparing Vocabulary
    # print("Preparing vocabulary..")

    stop = set(stopwords.words('english'))
    stop.add('/br')
    print(stop)


    # Positive to vectors
    positive_vocabulary = set(positive_model.wv.vocab).difference(stop)
    positive_vocabulary = [i for i in positive_vocabulary if can_be_adjective(i)]
    positive_vectors = []
    for sentence in positive_tokens:
        for word in sentence:
            if word in positive_vocabulary:
                positive_vectors.append(positive_model[word])
    positive_vectors = np.array(positive_vectors)

    # Negative to vectors
    negative_vocabulary = set(negative_model.wv.vocab) - stop
    negative_vocabulary = [i for i in negative_vocabulary if can_be_adjective(i)]
    negative_vectors = []
    for sentence in negative_token:
        for word in sentence:
            if word in negative_vocabulary:
                negative_vectors.append(negative_model[word])
    negative_vectors = np.array(negative_vectors)

    #Clustering
    print("Clustering..")
    print("Positive cluster: {}".format(positive_tokens))
    # pos_kmeans = KMeans(n_clusters=num_clusters, max_iter=5000).fit(s1)
    # pos_centers = pos_kmeans.cluster_centers_
    # pos_neigh = KNeighborsClassifier(n_neighbors=1)
    # pos_neigh.fit(s1, pos_kmeans.labels_)
    # neg_kmeans = KMeans(n_clusters=num_clusters, max_iter=5000).fit(s2)
    # neg_centers = neg_kmeans.cluster_centers_
    # neg_neigh = KNeighborsClassifier(n_neighbors=1)
    # neg_neigh.fit(s2, neg_kmeans.labels_)
    # Initalize a k-means object and use it to extract centroids
    positive_clusters = make_clusters(positive_vectors)

    print("-> Positive adjectives:")
    positive_min_dist = print_clusters_centroids_to_words(positive_clusters, positive_vocabulary, positive_model)
    negative_clusters = make_clusters(negative_vectors)

    print("-> Negative adjectives:")
    negative_min_dist = print_clusters_centroids_to_words(positive_clusters, negative_vocabulary, negative_model)

    # print_clusters(pos_clusters, cluster_word_dict(pos_clusters, positive_model))
    return (positive_min_dist, negative_min_dist)







if __name__ == "__main__":
    #Example
    df = pd.read_csv("Reviews.csv")

    ex_product = df[['Text', 'Score']][df['ProductId'] == "B007JFMH8M"]

    prod_positives = ex_product['Text'][ex_product['Score'] == 5].as_matrix()
    prod_negatives = ex_product['Text'][ex_product['Score'] <= 2].as_matrix()

    get_summary(prod_positives, prod_negatives)
