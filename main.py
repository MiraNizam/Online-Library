import argparse

import requests
from bs4 import BeautifulSoup
from check_for_redirect import check_for_redirect
from download_book import download_txt
from download_image import download_image
from parse_page import parse_book_page
from tqdm import tqdm
import sys
import logging


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
            url_d = f"https://tululu.org/txt.php?id={book_id}"
            url = f"https://tululu.org/b{book_id}/"
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, "lxml")
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
            stderr_file.write(f"Exception occurred. There was redirect.\n")
            logging.basicConfig(level=logging.INFO, format="%(asctime)s %(process)d %(levelname)s %(message)s")
            logging.info(f"Failed to download the book from the link {url}.")
            continue


if __name__ == "__main__":
    main()
