import re
import dataset
import requests
from bs4 import BeautifulSoup
import cloudscraper

db = dataset.connect("sqlite:///reviews.db")

session = cloudscraper.CloudScraper()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"
})

product_id = "1449355730"

def parse_reviews(response):
    bs = BeautifulSoup(response, "lxml")
    reply = bs.find("div", class_="review-views")
    reviews = []
    for fragment in reply.find_all("div", attrs={"data-hook": "review"}):

        review_id = fragment.get("id")
        title = fragment.find(class_="review-title").get_text(strip=True)
        review = fragment.find(class_="review-text").get_text(strip=True)
        review_cls = " ".join(fragment.find(class_="review-rating").get("class"))
        rating = re.search('a-star-(\d+)', review_cls).group(1)
        reviews.append({
            "review_id": review_id,
            "rating": rating,
            "title": title,
            "review": review 
        })
    
    return reviews

def get_reviews(product_id, page):
    url = "https://www.amazon.com/product-reviews/{}/ref=cm_cr_arp_d_paging_btm_next_{}".format(product_id, page)
    data = {
        "reviewerType": "all_reviews",
        "pageNumber": page,
        "ie": "UTF8"
    }
    r =session.get(url, params=data)

    reviews = parse_reviews(r.text)
    return reviews

page = 1
while True:
    print("Scraping page: ", page)
    reviews = get_reviews(product_id, page)
    if not reviews:
        break
    for review in reviews:
        print("-->", review["rating"], review["title"])
        db["reviews"].upsert(review, ["review_id"])
    page += 1
