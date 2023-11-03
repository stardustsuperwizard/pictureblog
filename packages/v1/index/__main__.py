import json

import jinja2
import jwt


ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
SECRET = os.environ['JWTKey']


def validate_jwt(encoded_jwt: str):
    try:
        data = jwt.decode(encoded_jwt.strip(), SECRET, algorithms=['HS256'])
    except Exception as e:
        data = False
    return data


def html_reponse(event):
    method = event.get('http', {}).get("method", "")
    
    template = ENVIRONMENT.get_template("base.html")
    if method.lower() == 'get':
        if event.get('http', {}).get('headers', {}).get('cookie'):
            cookie = dict(key_val_pair.split('=') for key_val_pair in event['http']['headers']['cookie'].split(';'))
            valid_token = validate_jwt(cookie['Token'])
            if valid_token:
                return {
                    "statusCode": 200,
                    "body": template.render(event = json.dumps(event), user = valid_token['user']),
                    "headers": {
                        "Content-Type": "text/html",
                    }
                }

    return {
        "statusCode": 200,
        "body": template.render(event = json.dumps(event)),
        "headers": {
            "Content-Type": "text/html",
        }
    }


def main(event, context):
    response = event
    if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
        response = f"<html><body><h1>Homepage</h1><p>{json.dumps(event, indent=4)}</p></body></html>"
    else:
        response = {
        "statusCode": 200,
        "body": response
    }
    return response
