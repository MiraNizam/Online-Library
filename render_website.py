from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server, shell


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        book_descriptions=get_book_descriptions(),
    )

    with open('rendered_index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def get_book_descriptions():
    with open("book_descriptions.json", "r") as file:
        book_descriptions_json = file.read()
    book_descriptions = json.loads(book_descriptions_json)
    return book_descriptions


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == "__main":
    main()
