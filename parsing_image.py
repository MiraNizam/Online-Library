import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_image(book_id: int) -> str:
    """Function collects the name of books from the site."""
    url = f"https://tululu.org/b{book_id}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    picture_tag = soup.find("div", class_="bookimage").find("img")["src"]
    picture_path = urljoin(url, picture_tag)
    return picture_path

