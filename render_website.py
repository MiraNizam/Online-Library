import argparse
import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked

BOOK_COUNT = 10


def create_parser():
    """create parser to add arguments"""
    parser = argparse.ArgumentParser(
        description="The script creates the site with books"
    )

    parser.add_argument(
        "--json_path",
        default="media/book_descriptions.json",
        type=str,
        help="path to JSON file, as default: '' "
    )
    return parser


def on_reload(json_path):
    with open(f"{json_path}", "r", encoding="utf-8") as file:
        book_descriptions = json.load(file)
    chunked_descriptions_by_pages = list(chunked(book_descriptions, BOOK_COUNT))

    page_folder = "pages"
    os.makedirs(page_folder, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("template.html")

    for number, page in enumerate(chunked_descriptions_by_pages, 1):
        page_path = os.path.join(page_folder, f"index{number}.html")
        rendered_page = template.render(
            book_descriptions=page,
            current_page=number,
            page_count=len(chunked_descriptions_by_pages)
        )

        with open(page_path, "w", encoding="utf-8") as file:
            file.write(rendered_page)


def main():
    parser = create_parser()
    args = parser.parse_args()
    json_path = args.json_path

    on_reload(json_path)
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".")


if __name__ == "__main__":
    main()
