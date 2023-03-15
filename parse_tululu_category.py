import argparse
import json
import logging
import os.path
import sys
import time
from parser import parse_book_page
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from check_for_redirect import check_for_redirect
from downloader import download_image, download_txt

logger = logging.getLogger(__file__)


def create_args(last_page):
    """create parser to add arguments"""
    parser = argparse.ArgumentParser(
        description="The script downloads books from the site https://tululu.org in the range id books"
    )
    parser.add_argument(
        "--start_page",
        default=1,
        type=int,
        help="the start position in range for parsing, default: 1",
    )
    parser.add_argument(
        "--end_page",
        default=last_page,
        type=int,
        help="the start position in range for parsing, default: the last page in category",
    )
    parser.add_argument(
        "--dest_folder",
        default="",
        type=str,
        help="path to the catalogue with parse result: images, books, JSON, as default: current folder"
    )
    parser.add_argument(
        "--skip_imgs",
        default=False,
        type=bool,
        help="Don't download images",
    )
    parser.add_argument(
        "--skip_txt",
        default=False,
        type=bool,
        help="Don't download txt",
    )
    parser.add_argument(
        "--json_path",
        default="",
        type=str,
        help="path to *.json file"
    )

    return parser


def define_last_page(url):
    """Func defines the first and the last pages from category"""
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    last_page = int(soup.select_one(".npage:last-child").text)
    return last_page


def parse_category(url, page_start: int, page_finish: int):
    """ Parse range of pages from sci-fi category. Return generator with book urls. """
    stderr_file = sys.stderr
    for page in range(page_start, page_finish):
        try:
            sci_fi_page = f"{url}{page}"
            response = requests.get(sci_fi_page)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            book_ids = soup.select(".d_book")
            for id in book_ids:
                book_url = urljoin(sci_fi_page, id.find("a")["href"])
                yield book_url
        except requests.exceptions.ConnectionError as error:
            logging.error("Lost connection to the site")
            print(f"{error} continue in 5 seconds")
            time.sleep(5)

            continue
        except requests.exceptions.HTTPError as error:
            stderr_file.write(f"Exception occurred. {error} \n")
            logging.error(f"HTTPError is raised. The link {sci_fi_page}.")
            continue
        except TypeError:
            continue


def save_to_json(book_descriptions: list, filepath: str):
    Path(filepath).mkdir(parents=True, exist_ok=True)
    json_filepath = os.path.join(filepath, "book_descriptions.json")
    with open(json_filepath, "w", encoding="utf8") as file:
        json.dump(book_descriptions, file, indent=4, ensure_ascii=False)


def main():
    logging.basicConfig(level=logging.ERROR, format="%(asctime)s %(process)d %(levelname)s %(message)s")
    logger.setLevel(logging.DEBUG)
    category_url = "https://tululu.org/l55/"
    stderr_file = sys.stderr
    last_page = define_last_page(category_url) + 1
    parser = create_args(last_page)
    args = parser.parse_args()
    start_page = args.start_page
    end_page = args.end_page
    images_folder = os.path.join(args.dest_folder, "images")
    txt_folder = os.path.join(args.dest_folder, "books")
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt
    json_path = os.path.join(args.json_path, "")
    book_descriptions = list()

    for book_url in parse_category(category_url, start_page, end_page):
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

            if not skip_imgs:
                img_path = download_image(picture_url, images_folder)
            else:
                img_path = "No picture"

            if not skip_txt:
                book_path = download_txt(book_response, filename, txt_folder)
            else:
                book_path = "No txt"

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
            logging.error("Lost connection to the site")
            print(f"{error} continue in 5 seconds")
            time.sleep(5)
            continue
        except requests.HTTPError:
            stderr_file.write(f"Exception occurred. There was redirect.\n")
            logging.error(f"HTTPError is raised. The link  {book_url}.")
            continue
        except TypeError:
            continue
    save_to_json(book_descriptions, json_path)


if __name__ == "__main__":
    main()
