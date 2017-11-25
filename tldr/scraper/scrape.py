from bs4 import BeautifulSoup, Comment
import re, itertools, random
import urllib
from datetime import datetime

#import generate_ngrams
import difflib

from time import sleep

AMAZON_ADV_SEARCH_BASE_URL = 'http://www.amazon.com/gp/search/ref=sr_adv_b/'

class Review:
    ''' simple class to hold together properties'''
    pass

def get_soup(url):
    '''
    Open the URL and make a Soup with the content
    '''
    # sleep(random.randrange(1,3)) # prevent too many requests at the same time
    try:
        content = urllib.urlopen(url).read()
    except:
        raise Exception('UrlOpenFail', url)

    soup = BeautifulSoup(content, "html.parser")
    return soup

def get_review_url(main_page):
    '''
    Get the URL that has the reviews off the main product page
    Tries by the item id, falls back on a structure approach
    '''
    # try by id (not always present)
    a=main_page.find(id="revSAR")    # returns an "a" tag
    if a:
        review_url = a.attrs['href'] # pull out the href
    else:
        # back-up to by structure
        reviews_summary = main_page.find(id="revSum")
        all_a = reviews_summary.find_all(href=re.compile('product-reviews'))
        if len(all_a):
            review_url = all_a[-1].attrs['href']
        else:
            print
            "No reviews found"
            return False
    return review_url

def get_num_each_rating(review_page):
    '''
    how many reviews of each rating?
    '''
    try:
        product_summary_div = review_page.find(id="productSummary")
        s = product_summary_div.find('b').string
        num_reviews = int(s.split(' ')[0].replace(',',''))
        num_reviews_by_star = []

        star_table = product_summary_div.find('table')
        for tr in star_table('tr'):
            s = tr('td')[-1].string.strip() # last td, take out white space
            if (len(s) > 2 and s[1:-1].isdigit()):
                n = s[1:-1].replace(',','') # take out ( ), strip comma
                num_reviews_by_star.append(int(n))

        return num_reviews_by_star
    except:
        raise Exception('NoRatingCountsFound')

def pull_out_reviews(review_page):
    '''
    This method is likely to break over time as it relies on very
    specific structure for the review
    Particularly, it depends on the review being embedded between
    "This review is from .." and "Help other customers .. "
    '''
    try:
        helpfulness_regex = re.compile(r'^\s*(\d+)\s+of\s+(\d+) people found the following review helpful\s*$')
        reviewer_href_regex = re.compile(r'/gp/pdp/profile/([^/])+')

        reviews = []

        # get the part of the page wth the reviews
        product_reviews_section = review_page.find(id="productReviews").find('td')

        boundaries = product_reviews_section.find_all(text=lambda text:isinstance(text, Comment))
        # dates = product_reviews_section.find_all('nobr')

        if (boundaries):
            for boundary in boundaries:
                review = Review()
                # get metadata

                date = boundary.find_next('nobr')
                try:
                    # parse the date string
                    review.date = datetime.strptime(date.text, '%B %d, %Y').date()
                except:
                    raise Exception('CouldNotParseDate')

                reviewer = boundary.find_next('a', href=reviewer_href_regex)
                reviewer_href = reviewer.attrs['href']
                # reviewer = (reviewer_id, reviewer_name, reviewer_url)
                review.reviewer_id = reviewer_href.split('/')[-1]
                review.reviewer_username = reviewer.text.strip('"')
                review.reviewer_url = reviewer_href

                texts = boundary.find_all_next(text=True)
                start = False
                skip = False
                review_text = ''
                for t in texts:
                    t = t.strip()
                    if start and t.startswith('Help other customers'):
                        break

                    helpfulness_match = helpfulness_regex.match(t)
                    if helpfulness_match:
                        helpfulness = (int(helpfulness_match.group(1)), int(helpfulness_match.group(2)))

                    if t.startswith('This review is from'):
                        start = True
                        # advance one more (the title)
                        skip = True
                        continue
                    if not start or skip:
                        skip = False
                        continue

                    if len(t):
                        review_text += t

                review.text = review_text.strip()
                review.word_count = sum([len(s) for s in generate_ngrams.get_tokenized_sentences(review.text)])

            # TODO: save token length
            reviews.append(review)
            helpfulness = False

        return reviews
    except:
        raise Exception('ReviewsNotFound')
