from flask import Flask, render_template, url_for, request

import tldr.scraper.amazon_review_retrieval as amazon
from tldr.word_embedding import summarizer as s

app= Flask(__name__)

@app.route('/home')
def index():
    url_for('static', filename='css/bootstrap.min.css', _external=True)
    url_for('static', filename='css/home.css', _external=True)
    return render_template('index.html')

@app.route('/review', methods=['GET','POST'])
def review():
    url_for('static', filename='css/bootstrap.min.css', _external=True)
    url_for('static', filename='css/home.css', _external=True)
    url = request.args.get('url')


    print("Downloading reviews..")
    soup = amazon.get_soup(url)
    name = amazon.get_title(soup)
    rating = amazon.get_average_rating(soup)
    reviews = amazon.get_all_reviews_in_all_pages(soup, url, limit=10)
    # print("*{}*\n {}\n".format(review['Score'], review['Text']))
    prod_positives = [review['Text'] for review in reviews if review['Score'] == 5]
    prod_negatives = [review['Text'] for review in reviews if review['Score'] <= 2]
    
    pros, cons = s.get_summary(prod_positives, prod_negatives)

    return render_template('review.html', data = [name, rating, pros, cons])


@app.errorhandler(404)
def error(e):
    url_for('static', filename='css/404.css', _external=True)
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='localhost')
