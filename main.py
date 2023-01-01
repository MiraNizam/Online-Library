import requests
from pathlib import Path

Path("books/").mkdir(parents=True, exist_ok=True)
for i in range(1, 11):
    url_template = f"https://tululu.org/txt.php?id={i}"
    response = requests.get(url_template)
    response.raise_for_status()

    filename = f"id{i}.txt"
    with open(f"books/{filename}", "w+", encoding="utf-8") as file:
        file.write(response.text)

