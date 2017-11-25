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

def get_reviews_ratings(soup_reviews_list):
    return [el.find_all('span', class_="a-icon-alt") for el in soup_reviews_list]

def get_reviews_text(soup_reviews_list):
    return [el.find_all('span', class_="a-size-base review-text") for el in soup_reviews_list]

def get_last_page_number(soup_page):
    ellippsis_button = soup_page.find_all('li', class_="a-disabled page-ellipsis")[0]
    last_page_button = ellippsis_button.find_next_sibling()
    return last_page_button.get_text()
