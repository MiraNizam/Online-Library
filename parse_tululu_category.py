import os.path
import json
import requests
from bs4 import BeautifulSoup
from check_for_redirect import check_for_redirect
from urllib.parse import urljoin
from parser import parse_book_page
from downloader import download_txt, download_image
import time
import logging
import sys


def parse_sci_fi_category(page_start: int = 1, page_finish: int = 4):
    """ Parse range of pages from sci-fi category. Return generator with book urls. """
    sci_fi_url = "https://tululu.org/l55/"
    for page in range(page_start, page_finish+1):
        sci_fi_page = f"{sci_fi_url}{page}"
        response = requests.get(sci_fi_page)
        response.raise_for_status()
        check_for_redirect(response)
        soup = BeautifulSoup(response.text, 'lxml')
        book_ids = soup.find_all("table", class_="d_book")
        for id in book_ids:
            book_url = urljoin(sci_fi_page, id.find("a")["href"])
            yield book_url


def save_to_json(book_descriptions, filepath: str = ""):
    json_filepath = os.path.join(filepath, "book_descriptions.json")
    with open(json_filepath, "w", encoding="utf8") as file:
        json.dump(book_descriptions, file, indent=4, ensure_ascii=False)


def main():
    stderr_file = sys.stderr
    book_descriptions = list()
    for book_url in parse_sci_fi_category():
        try:
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)

            soup = BeautifulSoup(response.text, "lxml")
            book_details = parse_book_page(soup, book_url)
            title = book_details["title"]
            picture_url = book_details["picture_url"]
            filename = f"{title}"
            book_response = requests.get(book_details["txt_url"])
            img_path = download_image(picture_url)
            book_path = download_txt(book_response, filename)
            book_description = {
                "title": book_details["title"],
                "author": book_details["author"],
                "img_path": img_path,
                "book_path": book_path,
                "comments": book_details["comments"],
                "genres": book_details["genres"],
            }
            book_descriptions.append(book_description)

        except requests.ConnectionError as error:
            print(f"{error} continue in 5 seconds")
            time.sleep(5)
            continue
        except requests.HTTPError:
            stderr_file.write(f"Exception occurred. There was redirect.\n")
            logging.basicConfig(level=logging.INFO, format="%(asctime)s %(process)d %(levelname)s %(message)s")
            logging.info(f"Failed to download the book from the link {book_url}.")
            continue
        except TypeError:
            continue
    save_to_json(book_descriptions)


if __name__ == "__main__":
    main()
