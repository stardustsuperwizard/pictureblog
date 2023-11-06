def main(event, method, token):
    content = f"You are only seeing this because you are logged in."
    return {
        "template": "index.html",
        "statusCode": 200,
        "message": "Hello World.",
        "data": {"content": content, 'token': token, 'event': event},
        "headers": {}
    }