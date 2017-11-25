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
    soup = amazon.get_soup(url)

