from bs4 import BeautifulSoup
import requests


def get_soup(url):
    '''
    Open the URL and make a Soup with the content
    '''
    content = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    soup = BeautifulSoup(content.text, "lxml")
    return soup

def get_title(soup_page):
    title = soup_page.find_all('title')[0].get_text()
    return title.lstrip("Amazon.com: Customer reviews: ")

def get_average_rating(soup_page):
    average = soup_page.find_all('span', class_="arp-rating-out-of-text")[0].get_text()
    return int(float(average.rstrip(" out of 5 stars")))



def get_reviews_html(soup_page):
    sp = soup_page.find_all('div', class_="a-section review")
    return sp


def get_reviews_ratings(soup_page_list):
    return [el.find('i', class_="review-rating") for el in soup_page_list]


def get_reviews_text(soup_page_list):
    return [el.find('span', class_="review-text") for el in soup_page_list]


def get_last_page_number(soup_page):
    ellipsis_button = soup_page.find_all('li', class_="a-disabled page-ellipsis")[0]
    last_page_button = ellipsis_button.find_next_sibling()
    return last_page_button.get_text()


def get_all_reviews_in_all_pages(first_page, url, limit=20):

    # Lambda function to flatten a list (list of list -> list)
    flatten = lambda l: [item for sublist in l for item in sublist]

    # Get the last page as an integer
    last_page = int(get_last_page_number(first_page))

    # List all the pages from 1 to last page
    pages = list()
    for i in range(1, min(limit, last_page) + 1):
        pages.append(get_soup(url+"&pageNumber={}".format(i)))

    # Download the review of all the pages
    reviews = list()
    for i, page in enumerate(pages):
        # print("Page {}".format(i+1))
        html_review = get_reviews_html(page)
        reviews_ratings = [r.get_text("|", strip=True) for r in get_reviews_ratings(html_review)]
        reviews_texts = [r.get_text("|", strip=True) for r in get_reviews_text(html_review)]
        # print("{}, {}".format(len(reviews_ratings), len(reviews_texts)))
        page_reviews = [{'Text': text, 'Score': float(rating.split()[0])} for rating, text in zip(reviews_ratings, reviews_texts)]
        reviews.extend(page_reviews)

    return reviews


