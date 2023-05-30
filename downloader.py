import os.path
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests
from pathvalidate import sanitize_filename


def download_txt(response, filename, folder):
    """Function for downloading text files.
    Args:
        response: Link to the text you want to download.
        filename (str): The name of the file to save with.
        folder (str): Folder where to save.
    returns:
        str: The path to the file where the text is saved.
    """

    Path(folder).mkdir(parents=True, exist_ok=True)
    checked_filename = sanitize_filename(filename)
    full_filename = f"{checked_filename}.txt"
    text_path = os.path.join(folder, full_filename)
    with open(text_path, "w+", encoding="utf-8") as file:
        file.write(response.text)
    return text_path


def download_image(url, folder):
    """Function for downloading images.
    Args:
        url (str): Link to the image you want to download.
        folder (str): Folder where to save.
    returns:
        str: The path to the file where the picture is saved.
    """
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = urlsplit(unquote(url)).path.split("/")[-1]
    picture_path = os.path.join(folder, filename)
    response = requests.get(url)
    response.raise_for_status()
    with open(picture_path, "wb") as file:
        file.write(response.content)
    return picture_path
