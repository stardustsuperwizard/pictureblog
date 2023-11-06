import os

import jwt

from . import router

SECRET = os.environ['JWTKey']

AUTHENTICATION_REQUIRED = True
METHODS = ["get", "post"]


# Validation Methods
def validate_jwt(encoded_jwt: str):
    try:
        data = jwt.decode(encoded_jwt.strip(), SECRET, algorithms=['HS256'])
    except Exception as e:
        data = False
    return data


def html_authentication(event):
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
    
    return False


def main(event, context):
    # Check if HTTP methods are valid.
    if event.get('http', {}).get('method', "") in METHODS: 
        pass
    else:
        return {
            "statusCode": 405,
            "body": {
                "message": "405 Method Not Allowed. Your request method is not supported."
            },
        }


    # Check if HTTP Headers are valid.
    if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
        pass
    elif "application/json" in event.get('http', {}).get('headers', {}).get("accept", ""):
        pass
    else:
        return {
        "statusCode": 403,
        "body": {"message": "403 Forbidden. Incorrect accept headers, please use either 'application/json' or 'text/html' in your request."},
    }


    # Check if authentication is required
    token = False
    if AUTHENTICATION_REQUIRED:
        if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
            token = html_authentication(event)
        elif "application/json" in event.get('http', {}).get('headers', {}).get("accept", ""):
            token = json_authenticated(event)
        
        if token == False:
            if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
                return {
                    "statusCode": 401,
                    "body": "<html><body><h1>401 Unauthorized</h1><p>You do not have valid authorization credentials.</p></body></html>",
                    "headers": {
                        "Content-Type": "text/html",
                    }
                }
            elif "application/json" in event.get('http', {}).get('headers', {}).get("accept", ""):
                return {
                    "statusCode": 401,
                    "body": { "message": "401 Unauthorized. You do not have valid authorization credentials.",
                        "data": {},
                        "event": event
                    },
                    "headers": {
                        "Content-Type": "application/json",
                    }
                }


    response_data = router.route(event, token)
    if "text/html" in event.get('http', {}).get('headers', {}).get("accept", ""):
        response_data['headers']['Content-Type'] = 'text/html'
        template = ENVIRONMENT.get_template(response_data['template'])
        page = template.render(event = json.dumps(event), response_data = response_data['data'])
        response = {
            "statusCode": response_data['statusCode'],
            "body": page,
            "headers": response_data['headers'],
        }
    elif "application/json" in event.get('http', {}).get('headers', {}).get("accept", ""):
        response_data['headers']['Content-Type'] = 'application/json'
        response = {
            "statusCode": response_data['statusCode'],
            "body": {
                "message": response_data['message'],
                "data": response_data['data'],
                "event": event,
                },
            "headers": response_data['headers']
        }
    else:
        response = {
        "statusCode": 418,
        "body": "<html><body><p>418 I'm a teapot</p><p>Technically, everything is okay...for some reason you are getting this message instead of what you actually wanted.</p></body></html>",
        "headers": {
            "Content-Type": "text/html",
        }
    }

    return response


#
# Debugging area:
# 
if __name__ == '__main__':
    response = main({'http':{'headers':{'cookie':'Token=athing', 'accept':'text/html'}}}, "")
    # response = main({}, "")
    print(response)