from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server, shell
from more_itertools import chunked
import os


def on_reload():
    with open("book_descriptions.json", "r") as file:
        book_descriptions_json = file.read()
    book_descriptions = json.loads(book_descriptions_json)
    chunked_descriptions_by_pages = list(chunked(book_descriptions, 20))

    path = "pages"
    os.makedirs(path, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    for number, page in enumerate(chunked_descriptions_by_pages, 1):
        page_path = os.path.join(path, f"index{number}.html")
        rendered_page = template.render(book_descriptions=page)

        with open(page_path, "w", encoding="utf-8") as file:
            file.write(rendered_page)



def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

main()

if __name__ == "__main":
    main()
