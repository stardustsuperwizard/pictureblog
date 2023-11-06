import json
import os

import jwt


SECRET = os.environ['JWTKey']

AUTHENTICATION_REQUIRED = True
METHODS = ["get", "post"]


def validate_jwt(encoded_jwt: str):
    try:
        data = jwt.decode(encoded_jwt.strip(), SECRET, algorithms=['HS256'])
    except Exception as e:
        data = False
    return data


def html_authentication(event):
    status = 418
    page = "<html><body><p>418 I'm a teapot</p><p>Technically, everything is okay...for some reason you are getting this message instead of what you actually wanted.</p></body></html>"    
    if event.get('http', {}).get('headers', {}).get('cookie'):
        cookies = [key_val_pair for key_val_pair in event['http']['headers']['cookie'].split(';')]
        for cookie in cookies:
            if 'Token=' in cookie:
                token = cookie.split('=')[1].strip()
                valid_token = validate_jwt(token)
                if valid_token:
                    return valid_token
    return False


def json_authentication(event):
    username = event.get('username')
    password = event.get('password')

    if not username or not password:
        return False

    if valid_token := create_jwt(username, password)
        return valid_token
    else:
        return False


def main(event, context):
    response = event
    token = False
    if event.get('http', {}).get('method', "") in METHODS: 
        if AUTHENTICATION_REQUIRED:
            if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
                token = html_authentication(event)
            elif "application/json" in event.get('http', {}).get('headers', {}).get("accept", ""):
                token = json_authenticated(event)
            else:
                return {
                    "statusCode": 403,
                    "body": {"message": "Incorrect headers."},
                }
    else:
        return {
            "statusCode": 405,
            "body": {
                "message": "405 Method Not Allowed. Your request method is not supported."
            },
        }

    
    return response


#
# Debugging area:
#a  a   
if __name__ == '__main__':
    response = main({'http':{'headers':{'cookie':'Token=athing', 'accept':'text/html'}}}, "")
    # response = main({}, "")
    print(response)