import argparse
import logging
import sys
import time
from parser import parse_book_page

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from check_for_redirect import check_for_redirect
from downloader import download_image, download_txt


def create_parse_args():
    """create parser to add arguments"""
    parser = argparse.ArgumentParser(
        description="The script downloads books from the site https://tululu.org in the range id books"
    )
    parser.add_argument(
        "--start_id",
        default=1,
        type=int,
        help="the start position in range for parsing, default: 1",
    )
    parser.add_argument(
        "--end_id",
        default=10,
        type=int,
        help="the end position in range for parsing, default: 10",
    )
    return parser


def main():

    stderr_file = sys.stderr
    parser = create_parse_args()
    args = parser.parse_args()

    for book_id in tqdm(range(args.start_id, args.end_id + 1)):
        try:
            txt_folder = "books"
            images_folder = "images"
            book_url = f"https://tululu.org/txt.php"
            page_url = f"https://tululu.org/b{book_id}/"
            payload = {"id": book_id}
            page_response = requests.get(page_url)
            page_response.raise_for_status()
            check_for_redirect(page_response)
            book_response = requests.get(book_url, params=payload)
            book_response.raise_for_status()
            check_for_redirect(book_response)
            soup = BeautifulSoup(page_response.text, "lxml")
            book_details = parse_book_page(soup, page_url)
            title = book_details["title"]
            picture_url = book_details["picture_url"]
            filename = f"{book_id}.{title}"
            download_txt(book_response, filename, txt_folder)
            download_image(picture_url, images_folder)
        except requests.ConnectionError as error:
            print(f"{error} continue in 5 seconds")
            time.sleep(5)
            continue
        except requests.HTTPError:
            stderr_file.write(f"Exception occurred. There was redirect.\n")
            logging.basicConfig(level=logging.INFO, format="%(asctime)s %(process)d %(levelname)s %(message)s")
            logging.info(f"Failed to download the book from the link {page_url}.")
            continue


if __name__ == "__main__":
    main()
