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
    for review in amazon.get_all_reviews_in_all_pages(url, limit=1):
        print("*{}*\n {}\n".format(review[0], review[1]))


if __name__ == "__main__":
    cli_interface()