from urllib.parse import urljoin


def parse_book_page(soup, url):
    """
    Function for parsing data from the site.
    Args:
        soup: variable type <class 'bs4.BeautifulSoup'> to parse information.
        url(str): Link to the book.
    returns:
        page (dict): Keys: "title", "author", "picture_url", "comments", "genres".
    """

    book_details_tag = soup.find("h1")
    book_details = list(map(lambda x: x.strip(), book_details_tag.text.split("::")))
    picture_tag = soup.select_one(".bookimage img")["src"]
    picture_url = urljoin(url, picture_tag)
    txt_tag = soup.select_one('.d_book [href^="/txt.php?id="]')["href"]
    txt_url = urljoin(url, txt_tag)
    comments_tag = soup.select(".texts .black")
    comments = [comment.text for comment in comments_tag]
    genres_tag = soup.select("span.d_book a")
    genres = [genre.get_text() for genre in genres_tag]
    page = {
        "title": book_details[0],
        "author": book_details[1],
        "picture_url": picture_url,
        "txt_url": txt_url,
        "comments": comments,
        "genres": genres,
    }
    return page
