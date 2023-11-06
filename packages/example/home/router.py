import jinja2

from pages import index


def route(event, path, method, token):
    if path == "":
        response = index.main(event, method, token)
    return response