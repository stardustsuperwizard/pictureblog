import datetime
import json
import logging

import jinja2


ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))


def html_reponse(event):
    method = event.get('http', {}).get('headers', {}).get("method", "")
    if event.get('cookie', ""):
        cookie = dict(key_val_pair.split('=') for key_val_pair in event['cookie'])
        template = ENVIRONMENT.get_template("base.html")
        return {
            "statusCode": 200,
            "body": template.render(event = json.dumps(event))
                "Set-Cookie": f"Token={cookie['Token']}; Max-Age=0",

        }
    else:
        template = ENVIRONMENT.get_template("base.html")
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