import json
import logging

import jinja2
import jwt


ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
SECRET = 'mysecret'


def create_jwt(user: str, password: str):
    encoded_jwt = jwt.encode({'user': user}, SECRET, algorithm='HS256')
    return encoded_jwt


def validate_jwt(jwt: str):
    data = jwt.decode(jwt, SECRET, algorithms=['HS256'])
    return data


def html_reponse(event):

    method = event.get('http', {}).get("method", "")
    if method.lower() == 'post':
        jwt = create_jwt(event['username'], event['password'])
        template = ENVIRONMENT.get_template("authenticated.html")
        return {
            "statusCode": 200,
            "body": template.render(event = json.dumps(event), user = event['username']),
            "headers": {
                "Set-Cookie": f"Token={jwt}",
                "Content-Type": "text/html",
            }
        }    
    elif method.lower() == 'get':
        if event.get('cookie', ""):
            cookie = dict(key_val_pair.split('=') for key_val_pair in event['cookie'])
            user_dict = validate_jwt(cookie)
            template = ENVIRONMENT.get_template("authenticated.html")
            return {
                "statusCode": 200,
                "body": template.render(event = json.dumps(event), user = user_dict['user']),
                "headers": {
                    "Content-Type": "text/html",
                }
            }         

        template = ENVIRONMENT.get_template("unauthenticated.html")
        return {
            "statusCode": 200,
            "body": template.render(event = json.dumps(event)),
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
    response = main({'http':{'method':'GET', 'headers':{'accept':'text/html'}}}, "")
    # response = main({}, "")
    print(response)