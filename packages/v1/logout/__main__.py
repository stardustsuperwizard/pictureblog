import datetime
import json
import logging

import jinja2


ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))


def html_reponse(event):
    method = event.get('http', {}).get("method", "")
    if event.get('http', {}).get('headers', {}).get('cookie'):
        cookie = dict(key_val_pair.split('=') for key_val_pair in event['http']['headers']['cookie'].split(';'))
        jwt = cookie['Token']
        template = ENVIRONMENT.get_template("base.html")
        return {
            "statusCode": 200,
            "body": template.render(event = json.dumps(event)),
            "headers":{
                "Content-Type": "text/html",
                "Set-Cookie": f"Token={jwt}; Max-Age=0; Secure; HttpOnly",
            }
        }
    else:
        template = ENVIRONMENT.get_template("base.html")
        return {
            "statusCode": 200,
            "body": template.render(event = json.dumps(event)),
            "headers":{
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
    response = main({'http':{'headers':{'cookie':'Token=athing', 'accept':'text/html'}}}, "")
    # response = main({}, "")
    print(response)