import base64
import datetime
import os

from string import Template

import jinja2
import jwt


ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
SECRET = os.environ['JWTSECRET']
CREDENTIALS = Template("$user:$password")


def create_jwt(user: str, password: str):
    presented_user = base64.b64encode(CREDENTIALS.substitute(user=user.lower(), password=password).encode())
    authorized_user = base64.b64encode(CREDENTIALS.substitute(user=os.environ['ADMIN_NAME'].lower(), password=os.environ['ADMIN_PASS']).encode())
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
    user = False
    template = ENVIRONMENT.get_template("index.html")

    if method.lower() == 'post':
        valid_token = create_jwt(event['username'], event['password'])
        if valid_token:
            return {
                "statusCode": 303,
                "headers": {
                    "Set-Cookie": f"Token={valid_token}; Path=/; Max-Age=300; Secure; HttpOnly",
                    "Location": "/api/auth/home",
                }
            }    
    elif method.lower() == 'get':
        if event.get('http', {}).get('headers', {}).get('cookie'):
            cookies = [key_val_pair for key_val_pair in event['http']['headers']['cookie'].split(';')]
            for cookie in cookies:
                if 'Token=' in cookie:
                    token = cookie.split('=')[1].strip()
                    valid_token = validate_jwt(token)
                    if valid_token:
                        return {
                            "statusCode": 303,
                            "headers": {
                                "Location": "/api/auth/home",
                            }
                        }

    return {
        "statusCode": 200,
        "body": template.render(),
        "headers": {
            "Content-Type": "text/html",
        }
    }    


def json_response(event):
    method = event.get('http', {}).get("method", "")
    if method.lower() == 'post':
        username = event.get('username')
        password = event.get('password')

        if not username or not password:
            return {
                "statusCode": 401,
                "body": {'message': 'username or password incorrect.', 'data': {}, 'event': event},
                "headers":{
                    "Content-Type": "application/json",
                }
            }            

        valid_token = create_jwt(username, password)
        if valid_token:
            return {
                "statusCode": 200,
                "body": {'message':'Login successful!', 'data': {'token': valid_token}, 'event': event},
                "headers": {
                    "Content-Type": "application/json",
                }
            }  

    else:
        return {
            "statusCode": 401,
            "body": {'message': 'Log in.', 'data': {}, 'event': event},
            "headers":{
                "Content-Type": "application/json",
            }
        }


def main(event, context):
    response = {}
    if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
        response = html_reponse(event)
    else:
        response = json_response(event)
    return response


#
# Debugging area:
#
if __name__ == '__main__':
    # response = main({'http':{'method':'GET', 'headers':{'cookie':'Token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.6O7zatr8KRQaz91wY--6IhVTc3MqGl0fDToaMihUahA', 'accept':'text/html'}}}, "")
    # response = main({'http':{'method':'GET', 'headers':{'accept':'text/html'}}}, "")
    response = main({}, "")
    print(response)