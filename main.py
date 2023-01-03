import requests
from pathlib import Path
from download_book import download_txt
from download_image import download_image
from parsing_book_name import parse_book_name
from parsing_image import parse_image


def main():
    for book_id in range(3, 7):
        url = f"https://tululu.org/txt.php?id={book_id}"
        filename = f"{book_id}. {parse_book_name(book_id)}"
        download_txt(url, filename)
        download_image(parse_image(book_id))


if __name__ == "__main__":
    main()
