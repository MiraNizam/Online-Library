from download_book import download_txt
from download_image import download_image
from parse_page import parse_book_page
import requests
from bs4 import BeautifulSoup
from check_for_redirect import check_for_redirect


def main():
    for book_id in range(5, 7):
        try:
            url_d = f"https://tululu.org/txt.php?id={book_id}"
            url = f"https://tululu.org/b{book_id}/"
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            book_details = parse_book_page(soup, url)
            title = book_details["title"]
            author = book_details["author"]
            picture_url = book_details["picture_url"]
            comments = book_details["comments"]
            genres = book_details["genres"]
            filename = f"{book_id}.{title}"
            download_txt(url_d, filename)
            download_image(picture_url)
        except requests.HTTPError:
            continue


if __name__ == "__main__":
    main()
