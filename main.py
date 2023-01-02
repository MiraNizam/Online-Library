import requests
from pathlib import Path
from download_book import download_txt
from parsing_book_name import parse_book_name


def main():
    for book_id in range(1, 11):
        url = f"https://tululu.org/txt.php?id={book_id}"
        filename = f"{book_id}. {parse_book_name(book_id)}"
        download_txt(url, filename)


if __name__ == "__main__":
    main()
