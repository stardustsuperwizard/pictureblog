import json
import logging

import jinja2
import jwt


SECRET = 'mysecret'


def create_jwt(user: str, password: str):
    encoded_jwt = jwt.encode({'user': user}, SECRETKEY, algorithm='HS256')
    return encoded_jwt


def validate_jwt(jwt: str):
    data = jwt.decode(jwt, SECRET, algorithms=['HS256'])
    return data


def html_reponse(event):
    method = event.get('http', {}).get('headers', {}).get("method", "")
    if method.lower() == 'post':
        jwt = create_jwt(event['username'], event['password'])
        environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
        template = environment.get_template("authenticated.html")
        return {
            "statusCode": 200,
            "body": template.render(event = json.dumps(event)),
            "headers": {
                "Set-Cookie": f"Token={jwt}",
                "Content-Type": "text/html"
            }
        }    
    else:
        environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
        template = environment.get_template("unauthenticated.html")
        return {
            "statusCode": 200,
            "body": template.render(event = json.dumps(event))
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
# if __name__ == '__main__':
#     response = main({'http':{'headers':{'accept':'text/html'}}}, "")
#     # response = main({}, "")
#     print(response)