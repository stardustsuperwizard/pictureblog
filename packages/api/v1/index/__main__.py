import logging


def authentication(req: str):
    token = None
    if 'token' in req.get('headers', {}):
        token = True
    return token


def main(event, context):
    status = 200

    if authentication(event.get('http', {})):
        response = {"greeting": f"hello Mike!"}
    else:
        if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
            status = 401
            response = "<html><body><h1>Valid credentials required.</h1></body></html>"
        else:
            status = 401
            response = {"message": "Valid credentials required."}
    
    return {
        "statusCode": status,
        "body": response
    }