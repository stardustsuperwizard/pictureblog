def main(event, method, token):
    if token:
        content = f"Hello, {token['user']}"
    else:
        content = "Hello, stranger!"
    return {
        "template": "index.html",
        "statusCode": 200,
        "message": "Hello World.",
        "data": {"content": content, "token": token},
        "headers": {}
    }