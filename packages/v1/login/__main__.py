import base64
import datetime
import json
import logging
import os

from string import Template

import jinja2
import jwt


ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
SECRET = os.environ['JWTKey']
CREDENTIALS = Template("$user:$password")


def create_jwt(user: str, password: str):
    presented_user = base64.b64encode(CREDENTIALS.substitute(user=user, password=password).encode())
    authorized_user = base64.b64encode(CREDENTIALS.substitute(user=os.environ['ADMIN_NAME'], password=os.environ['ADMIN_PASS']).encode())
    if presented_user == authorized_user:
        return jwt.encode({'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=300), 'user': user}, SECRET, algorithm='HS256')
    return False


def validate_jwt(encoded_jwt: str):
    try:
        data = jwt.decode(encoded_jwt.strip(), SECRET, algorithms=['HS256'])
    except Exception as e:
        data = False
    return data


def html_reponse(event):
    method = event.get('http', {}).get("method", "")
    
    template = ENVIRONMENT.get_template("authenticated.html")
    if method.lower() == 'post':
        valid_token = create_jwt(event['username'], event['password'])
        if valid_token:
            return {
                "statusCode": 200,
                "body": template.render(event = json.dumps(event), user = event['username']),
                "headers": {
                    "Set-Cookie": f"Token={valid_token}; Max-Age=300; Secure; HttpOnly",
                    "Content-Type": "text/html",
                }
            }    
    elif method.lower() == 'get':
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

    template = ENVIRONMENT.get_template("unauthenticated.html")
    return {
        "statusCode": 200,
        "body": template.render(event = json.dumps(event), env = os.environ['ADMIN_NAME']),
        "headers": {
            "Content-Type": "text/html",
        }
    }    


def main(event, context):
    response = {}
    if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
        response = html_reponse(event)
    else:
        response = {
        "statusCode": 200,
        "body": response
    }
    return response


#
# Debugging area:
#
if __name__ == '__main__':
    # response = main({'http':{'method':'GET', 'headers':{'cookie':'Token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.6O7zatr8KRQaz91wY--6IhVTc3MqGl0fDToaMihUahA', 'accept':'text/html'}}}, "")
    response = main({'http':{'method':'GET', 'headers':{'accept':'text/html'}}}, "")
    # response = main({}, "")
    print(response)