from download_book import download_txt
from download_image import download_image
from parse_page import parse_book_page
import requests
from bs4 import BeautifulSoup
from check_for_redirect import check_for_redirect
import argparse
from tqdm import tqdm


def parse_cmd_args():
    """create parser to add arguments"""
    parser = argparse.ArgumentParser(
        description="The script downloads books from the site https://tululu.org in the range id books"
    )
    parser.add_argument("--start_id", default=1, type=int, help="the start position in range for parsing, default: 1")
    parser.add_argument("--end_id", default=10, type=int, help="the end position in range for parsing, default: 10")
    return parser


def main():
    parser = parse_cmd_args()
    args = parser.parse_args()
    for book_id in tqdm(range(args.start_id, args.end_id+1)):
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
