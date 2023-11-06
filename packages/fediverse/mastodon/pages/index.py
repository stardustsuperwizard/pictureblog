def main(event, method, token):
    return {
        "template": "index.html",
        "statusCode": 200,
        "message": "Hello World.",
        "data": {"content": "Hello World!"},
        "headers": {}
    }