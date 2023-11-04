import json
import os
import uuid

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
    status = 200
    
    user = False
    if method.lower() == 'delete':
        if event.get('http', {}).get('headers', {}).get('cookie'):
            cookies = [key_val_pair for key_val_pair in event['http']['headers']['cookie'].split(';')]
            for cookie in cookies:
                if 'Token=' in cookie:
                    token = cookie.split('=')[1].strip()
                    valid_token = validate_jwt(cookie['Token'])
                    if valid_token:
                        user = valid_token['user']
                        template = ENVIRONMENT.get_template("index.html")
                        page = template.render(event = json.dumps(event))
                        return {
                            "statusCode": status,
                            "body": page,
                            "headers": {
                                "Content-Type": "text/html",
                            }
                        }
                    else:
                        status = 401
                        template = ENVIRONMENT.get_template("401.html")
                        page = template.render(event = json.dumps(event))
                else:
                    status = 401
                    template = ENVIRONMENT.get_template("401.html")
                    page = template.render(event = json.dumps(event))
        else:
            status = 401
            template = ENVIRONMENT.get_template("401.html")
            page = template.render(event = json.dumps(event))
    else:
        status = 405
        template = ENVIRONMENT.get_template("405.html")
        page = template.render(event = json.dumps(event))    

    return {
        "statusCode": status,
        "body": page,
        "headers": {
            "Content-Type": "text/html",
        }
    }


def main(event, context):
    response = event
    if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
        response = html_reponse(event)
    else:
        response = {
        "statusCode": 200,
        "body": {},
    } 
    return response


#
# Debugging area:
#
# if __name__ == '__main__':
#     response = main({'http':{'headers':{'cookie':'Token=athing', 'accept':'text/html'}}}, "")
#     # response = main({}, "")
#     print(response)