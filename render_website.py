import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked
import argparse


def create_parser():
    """create parser to add arguments"""
    parser = argparse.ArgumentParser(
        description="The script creates the site with books"
    )

    parser.add_argument(
        "--json_path",
        default="media",
        type=str,
        help="path to JSON file, as default: media"
    )
    return parser


def on_reload(json_path="media"):
    with open(f"{json_path}/book_descriptions.json", "r") as file:
        book_descriptions_json = file.read()
    book_descriptions = json.loads(book_descriptions_json)
    chunked_descriptions_by_pages = list(chunked(book_descriptions, 10))

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
    json_path = os.path.join(args.json_path, "")

    on_reload(json_path)
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".")


if __name__ == "__main__":
    main()
