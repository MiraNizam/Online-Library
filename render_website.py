from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('index.html')

rendered_page = template.render(
    book_title="Бал хищников",
)

with open('rendered_index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)
