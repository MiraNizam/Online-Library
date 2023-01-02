import os.path
from pathlib import Path
import requests
from pathvalidate import sanitize_filename
from check_for_redirect import check_for_redirect


def download_txt(url, filename, folder='books/'):
    """Function for downloading text files.
     Args:
         url (str): Link to the text you want to download.
         filename (str): The name of the file to save with.
         folder (str): Folder where to save.
     returns:
         str: The path to the file where the text is saved.
    """
    Path(folder).mkdir(parents=True, exist_ok=True)
    checked_filename = sanitize_filename(filename)
    full_filename = f"{checked_filename}.txt"
    text_path = os.path.join(folder, full_filename)
    try:
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)
        with open(text_path, "w+", encoding="utf-8") as file:
            file.write(response.text)
    except requests.HTTPError:
        pass
    return text_path
