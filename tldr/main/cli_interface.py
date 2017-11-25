"""
I love CLI!
"""

import tldr.scraper.amazon_review_retrieval as amazon

def cli_interface():
    print("""<!--       _
       .__(.)< (MEOW)
        \___)   
 ~~~~~~~~~~~~~~~~~~-->""")
    url = input("Please, paste the URL to the reviews.\n>>> ")
    url = url.strip()
    for review in amazon.get_all_reviews_in_all_pages(url):
        print("{}:\t {}".format(review[0], review[1]))
    print(amazon.get_all_reviews_in_all_pages(url, limit=5))

if __name__ == "__main__":
    cli_interface()