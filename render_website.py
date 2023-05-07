from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server, shell
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        book_descriptions_by_two=get_book_descriptions(),
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def get_book_descriptions():
    with open("book_descriptions.json", "r") as file:
        book_descriptions_json = file.read()
    book_descriptions = json.loads(book_descriptions_json)
    book_descriptions_by_two = list(chunked(book_descriptions, 2))
    print(*book_descriptions_by_two, sep="\n" )
    return book_descriptions_by_two


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

main()

# if __name__ == "__main":
#     main()
