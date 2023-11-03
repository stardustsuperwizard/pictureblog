import json
import logging


def main(event, context):
    status = 200
    if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
        response = f"<html><body><h1>{json.dumps(event, indent=4)}</h1></body></html>"
    else:
        response = {"message": event}
    return {
        "statusCode": status,
        "body": response
    }

