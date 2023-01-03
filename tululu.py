import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_page(start: int, stop: int) -> str:
    for id in range(start, stop):
        url = f"https://tululu.org/b{id}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        book_details_tag = soup.find("h1")
        book_details = list(map(lambda x: x.strip(), book_details_tag.text.split("::")))
        picture_tag = soup.find("div", class_="bookimage").find("img")["src"]
        picture_url = urljoin(url, picture_tag)
        comments_tag = soup.select(".texts > .black")
        comments = [comment.text for comment in comments_tag]
        page = {
            "title": book_details[0],
            "author": book_details[1],
            "picture_url": picture_url,
            "comments": comments,
        }
        print(page["title"])
        print(page["author"])
        print(page["picture_url"])
        print(page["comments"])




print(parse_page(5, 6))
