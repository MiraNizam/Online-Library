import os.path
from pathlib import Path
import requests
from check_for_redirect import check_for_redirect
from urllib.parse import urlsplit, unquote


def download_image(url, folder='images/'):
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
    print(picture_path)
    try:
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)
        with open(picture_path, "wb") as file:
            file.write(response.content)
    except requests.HTTPError:
        pass
    return picture_path
