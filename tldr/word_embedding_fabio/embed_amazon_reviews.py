from tldr.word_embedding_fabio import word_to_vec as w2v
import nltk


def embed_amazon_reviews(review_list):
    tokenizer = w2v.get_punktuation_tokenizer()

    sentences = list()  # Initialize an empty list of sentences

    for review in review_list:
        sentences.append(w2v.review_to_sentences(review, tokenizer, remove_stopwords=True))

    return w2v.train_model(sentences)


if __name__ == "__main__":
    import pandas as pd
    food = pd.read_csv('dataset/amazon_fine_food/Reviews.csv')
    embed_amazon_reviews(food['Text'])