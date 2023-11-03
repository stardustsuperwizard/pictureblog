import logging


def main(event, context):
    status = 200
    message = "Welcome to the API!"
    if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
        response = f"<html><body><h1>{message}</h1></body></html>"
    else:
        response = {"message": message}
    return {
        "statusCode": status,
        "body": response
    }

