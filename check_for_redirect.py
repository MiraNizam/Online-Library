import requests


def check_for_redirect(response):
    """Takes a response object as input, and checks for redirection"""
    if response.history:
        raise requests.HTTPError