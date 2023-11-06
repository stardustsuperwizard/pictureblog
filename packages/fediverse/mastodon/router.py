import jinja2


def route(event, token):
    response = {
        "template": "index.html",
        "statusCode": 200,
        "message": "Hello World.",
        "data": {"content": "Hello World!"},
        "headers": {}
    }
    return response