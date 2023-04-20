from jinja2 import Environment, FileSystemLoader, select_autoescape
import json


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


def get_book_descriptions():
    with open("book_descriptions.json", "r") as file:
        book_descriptions_json = file.read()
    book_descriptions = json.loads(book_descriptions_json)
    return book_descriptions


rendered_page = template.render(
    book_descriptions=get_book_descriptions(),
)

with open('rendered_index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)
