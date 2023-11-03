import json
import logging

import jinja2


def html_reponse(event):
    environment = jinja2.Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("template.html")
    return {
        "statusCode": 200,
        "body": template.render()
    }


def main(event, context):
    response = {}
    if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
        reponse = html_reponse(event)
    else:
        response = {
        "statusCode": 200,
        "body": response
    }
    return response

