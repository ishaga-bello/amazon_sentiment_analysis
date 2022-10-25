import json, re
import dataset
import requests
from bs4 import BeautifulSoup

db = dataset.connect("sqlite:///reviews.db")

review_url = "https://www.amazon.com/hz/reviews-render/ajax/reviews/get/"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"
})

product_id = "1449355730"
session.get('https://www.amazon.com/product-reviews/{}/'.format(product_id))

def parse_reviews(reply):
    reviews = []
    for fragment in reply.split("&&&"):
        if not fragment.strip():
            continue
        json_fragment = json.loads(fragment)
        if json_fragment[0] != "append" or not "html" in json_fragment[2]:
            continue
        bs = BeautifulSoup(json_fragment[2], "lxml")
        div = bs.find("div", class_="review")
        if not div:
            continue

        review_id = div.get("id")
        title = bs.find(class_="review-title").get_text(strip=True)
        review = bs.find(class_="review-text").get_text(strip=True)
        review_cls = " ".join(bs.find(class_="review-rating").get("class"))
        rating = re.search('a-star-(\d+)', review_cls).group(1)
        reviews.append({
            "review_id": review_id,
            "rating": rating,
            "title": title,
            "review": review 
        })
    
    return reviews

def get_reviews(product_id, page):
    data = {
        "sortBy": "",
        "reviewerType": "all_reviews",
        "formatType": "",
        "mediaType": "",
        "filterByStar": "all_stars",
        "pageNumber": page,
        "filterByKeyword": "",
        "shouldAppend": "undefined",
        "deviceType": "desktop",
        "reftag": "cm_cr_arp_d_paging_btm_next_{}".format(page),
        "pageSize": 10,
        "asin": product_id,
        "scope": "reviewAjax0"
    }
    r = session.post(review_url+"ref="+data["reftag"], data=data)

    reviews = parse_reviews(r.text)
    return reviews


# page = 1
# while True:
#     print("Scraping page: ", page)
#     reviews = get_reviews(product_id, page)
#     print(reviews)
#     # if not reviews:
#     #     break
#     # for review in reviews:
#     #     print("-->", review["rating"], review["title"])
#     #     # db["reviews"].upsert(review, ["review_id"])
#     page += 1
#     sleep(5)

for page in range(10):
    print("Scraping page: ", page)
    reviews = get_reviews(product_id, page)
    print(reviews)
