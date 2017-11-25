import os
import re
import time

from bs4 import BeautifulSoup
import logging
from gensim.models import word2vec
import gensim
from nltk.corpus import stopwords
import nltk.data
from sklearn.cluster import KMeans
import time

THIS_FILE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))
NLTK_SAVE_DIR = os.path.join(os.path.join(THIS_FILE_FOLDER,
                                          "NLTK"))

# Configure logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


# Keggle default
def train_model(sentences, min_word_count=40, context=10):
    """

    Parameters
    ----------
    sentences: list of str
        sentences to be analysed
    min_word_count: int
        minimum number of words to count
    context:
        window of neighbouring words to determine context

    Returns
    -------
    word2vec model

    """
    # Set values for various parameters
    num_features = 300  # Word vector dimensionality
    num_workers = 8  # Number of threads to run in parallel
    downsampling = 1e-3  # Downsample setting for frequent words

    return word2vec.Word2Vec(sentences, workers=num_workers,
                             size=num_features, min_count=min_word_count,
                             window=context, sample=downsampling)

def review_to_wordlist(review_text, remove_stopwords=False):
    # 2. Remove non-letters
    review_text = re.sub("[^a-zA-Z]", " ", review_text)
    #
    # 3. Convert words to lower case and split them
    words = review_text.lower().split()
    #
    # 4. Optionally remove stop words (false by default)
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if w not in stops]
    #
    # 5. Return a list of words
    return words


# Get words like new_york
def get_multiwords(sentences):
    return gensim.models.Phrases(sentences)

# Downloads nltk tokens if you don't have them
def download_punkt():
    if not os.path.exists(NLTK_SAVE_DIR):
        os.mkdir(NLTK_SAVE_DIR)

    nltk.download('punkt', download_dir=NLTK_SAVE_DIR)

# Get the punctuation tokenizer
def get_punktuation_tokenizer():

    punkt_path = os.path.join(NLTK_SAVE_DIR,
                                           'tokenizers',
                                           'punkt',
                                           'english.pickle')

    try:
        return nltk.data.load(punkt_path)
    except LookupError as e:
        print("Punkt not found, downloading punkt..")
        download_punkt()
        return nltk.data.load(punkt_path)




# Define a function to split a review into parsed sentences (lists of words)
def review_to_sentences(review, tokenizer, remove_stopwords=False):
    # Function to split a review into parsed sentences. Returns a
    # list of sentences, where each sentence is a list of words
    #
    # 1. Use the NLTK tokenizer to split the paragraph into sentences
    raw_sentences = tokenizer.tokenize(review.strip())
    #
    # 2. Loop over each sentence
    sentences = []
    for raw_sentence in raw_sentences:
        # If a sentence is empty, skip it
        if len(raw_sentence) > 0:
            # Otherwise, call review_to_wordlist to get a list of words
            sentences.append(review_to_wordlist(raw_sentence,
                             remove_stopwords))
    #
    # Return the list of sentences (each sentence is a list of words,
    # so this returns a list of lists
    return sentences


def scan_all_sentences(list_of_sentences, update_frequency=50):
    sentences = []  # Initialize an empty list of sentences
    tokenizer = get_punktuation_tokenizer()

    for i, sensence in enumerate(list_of_sentences):
        # Print some useful output
        if i % update_frequency:
            print(str(i) + " of " + str(len(list_of_sentences)))
        sentences += review_to_sentences(sensence, tokenizer)

    return sentences


def make_clusters(model):
    start = time.time()  # Start time

    # Set "k" (num_clusters) to be 1/5th of the vocabulary size, or an
    # average of 5 words per cluster
    word_vectors = model.syn0
    num_clusters = int(word_vectors.shape[0] / 5)

    # Initalize a k-means object and use it to extract centroids
    kmeans_clustering = KMeans(n_clusters=num_clusters, n_jobs=-1)
    idx = kmeans_clustering.fit_predict(word_vectors)

    # Get the end time and print how long the process took
    end = time.time()
    elapsed = end - start
    print("Time taken for K Means clustering: " + elapsed + "seconds.")

    return idx


def cluster_word_dict(idx, model):
    return dict(zip(model.index2word, idx))


def print_clusters(cluster, cluster_word_dict, amount=-1):

    if amount == -1:
        amount = len(cluster)

    for cluster in range(amount):
        #
        # Print the cluster number
        print("Cluster: " + str(cluster))
        #
        # Find all of the words for that cluster number, and print them out
        words = []
        for i, value in enumerate(cluster_word_dict.values()):
            if (value == cluster):
                c_keys = list(cluster_word_dict.keys())
                words.append(c_keys[i])
        print(str(words))