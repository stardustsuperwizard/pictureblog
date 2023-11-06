import json
import os

import jinja2
import jwt

from . import router


ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
SECRET = os.environ['JWTKey']


def validate_jwt(encoded_jwt: str):
    try:
        data = jwt.decode(encoded_jwt.strip(), SECRET, algorithms=['HS256'])
    except Exception as e:
        data = False
    return data


def authenticated(event):
    method = event.get('http', {}).get("method", "")
    status = 418
    page = "<html><body><p>418 I'm a teapot</p><p>Technically, everything is okay...for some reason you are getting this message instead of what you actually wanted.</p></body></html>"    
    
    user = False
    if method.lower() in ['get', 'post']:
        if event.get('http', {}).get('headers', {}).get('cookie'):
            cookies = [key_val_pair for key_val_pair in event['http']['headers']['cookie'].split(';')]
            for cookie in cookies:
                if 'Token=' in cookie:
                    token = cookie.split('=')[1].strip()
                    valid_token = validate_jwt(token)
                    if valid_token:
                        r = router.route(event, valid_token)
                        template = ENVIRONMENT.get_template(r['template'])
                        page = template.render(page_data = r['body']['data'])
                        headers = r['headers']
                        return {
                            "statusCode": r['statusCode'],
                            "body": page,
                            "headers": headers
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


def unauthenticated(event):
    method = event.get('http', {}).get("method", "")
    status = 418
    page = "<html><body><p>418 I'm a teapot</p><p>Technically, everything is okay...for some reason you are getting this message instead of what you actually wanted.</p></body></html>"    
    
    if method.lower() in ['get', 'post']:
        r = router.route(event, valid_token)
        template = ENVIRONMENT.get_template(r['template'])
        page = template.render(page_data = r['body']['data'])
        headers = r['headers']
        return {
            "statusCode": r['statusCode'],
            "body": page,
            "headers": headers
        }
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


#
# Debugging area:
#
if __name__ == '__main__':
    response = main({'http':{'headers':{'cookie':'Token=athing', 'accept':'text/html'}}}, "")
    # response = main({}, "")
    print(response)