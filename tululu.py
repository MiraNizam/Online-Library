import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_page(url: str) -> dict:
    """
    Function for parsing data from the site.
    Args:
        url (str): Link to the site you want to parse.
    returns:
        page (dict): Keys: "title", "author", "picture_url", "comments", "genres".
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_details_tag = soup.find("h1")
    book_details = list(map(lambda x: x.strip(), book_details_tag.text.split("::")))
    picture_tag = soup.find("div", class_="bookimage").find("img")["src"]
    picture_url = urljoin(url, picture_tag)
    comments_tag = soup.select(".texts > .black")
    comments = [comment.text for comment in comments_tag]
    genres_tag = soup.find("span", class_="d_book").find_all("a")
    genres = [genre.get_text() for genre in genres_tag]
    page = {
        "title": book_details[0],
        "author": book_details[1],
        "picture_url": picture_url,
        "comments": comments,
        "genres": genres,
    }
    return page
