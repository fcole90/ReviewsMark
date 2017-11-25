from tldr.word_embedding import word_to_vect as w2v
import nltk


def embed_amazon_reviews(review_list):
    tokenizer = w2v.get_punktuation_tokenizer()

    sentences = list()  # Initialize an empty list of sentences

    for review in review_list:
        sentences = w2v.review_to_sentences(review, tokenizer)

    w2v.train_model(sentences)


if __name__ == "__main__":
    embed_amazon_reviews(['dummy text!'])