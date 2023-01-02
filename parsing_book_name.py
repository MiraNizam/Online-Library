import requests
from bs4 import BeautifulSoup


def parse_book_name(book_id: int) -> str:
    """Function collects the name of books from the site."""
    url = f"https://tululu.org/b{book_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find("h1")
    title_text = list(map(lambda x: x.strip(), (title_tag.text).split("::")))
    return title_text[0]
