from bs4 import BeautifulSoup
import requests


def get_soup(url):
    '''
    Open the URL and make a Soup with the content
    '''
    content = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    soup = BeautifulSoup(content.text, "lxml")
    return soup

def get_reviews_html(soup_page):
    return soup_page.find_all('div', class_="a-section review")

def get_reviews_ratings(soup_page):
    return soup_page.find_all('span', class_="a-icon-alt")

def get_reviews_text(soup_page):
    return soup_page.find_all('span', class_="a-size-base review-text")

def get_last_page_number(soup_page):
    ellippsis_button = soup_page.find_all('li', class_="a-disabled page-ellipsis")[0]
    last_page_button = ellippsis_button.find_next_sibling()
    return last_page_button.get_text()

def get_all_reviews_in_all_pages(url, limit=20):

    # Lambda function to flatten a list (list of list -> list)
    flatten = lambda l: [item for sublist in l for item in sublist]

    first_page = get_soup(url)

    # Get the last page as an integer
    last_page = int(get_last_page_number(first_page))

    # List all the pages from 1 to last page
    pages = list()
    for i in range(1, min(limit, last_page) + 1):
        pages.append(get_soup(url+"&pageNumber={}".format(i)))

    # Download the review of all the pages
    reviews = list()
    for page in pages:
        reviews_texts = [r.get_text("|", strip=True) for r in get_reviews_text(page)]
        reviews_ratings = [r.get_text("|", strip=True) for r in get_reviews_ratings(page)]

        page_reviews = zip(reviews_ratings, reviews_texts)
        reviews.extend(page_reviews)

    return reviews


