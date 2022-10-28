import requests

url = "https://tululu.org/txt.php?id=32168"
response = requests.get(url)
response.raise_for_status()

filename = "Пески Марса. Кларк Артур"
with open(filename, "w+", encoding="utf-8") as file:
    book = file.write(response.text)

new_book = book.replace("\xa0", " ")


