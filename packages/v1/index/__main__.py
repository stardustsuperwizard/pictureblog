import json
import os

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
    
    user = False
    template = ENVIRONMENT.get_template("index.html")
    
    if event.get('http', {}).get('headers', {}).get('cookie'):
        cookies = [key_val_pair for key_val_pair in event['http']['headers']['cookie'].split(';')]
        for cookie in cookies:
            if 'Token=' in cookie:
                token = cookie.split('=')[1].strip()
                valid_token = validate_jwt(token)
                if valid_token:
                    user = valid_token['user']

    return {
        "statusCode": 200,
        "body": template.render(event = json.dumps(event), user = user),
        "headers": {
            "Content-Type": "text/html",
        }
    }


def json_response(event):
    user = 'stranger'
    if event.get('token'):
        valid_token = validate_jwt(event['token'])
        if valid_token:
            user = valid_token['user']

    return {
        "statusCode": 200,
        "body": {'message': f'Hello, {user}!', 'event': event},
        "headers": {
            "Content-Type": "application/json",
        }
    } 


def main(event, context):
    response = event
    if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
        response = html_reponse(event)
    else:
        response = json_response(event)
    return response


#
# Debugging area:
#
# if __name__ == '__main__':
#     response = main({'http':{'headers':{'cookie':'Token=athing', 'accept':'text/html'}}}, "")
#     # response = main({}, "")
#     print(response)