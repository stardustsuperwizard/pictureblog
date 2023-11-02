import logging

from functools import wraps


class WebApp:
    def __init__(self, event):
        self.event = event
        self.router()
        

    def router(self):
        self.routes = [
        {
            "path": "",
            "method": "GET",
            "function": self.index
        },
        {
            "path": "/",
            "method": "GET",
            "function": self.index
        },
        {
            "path": "/hello",
            "method": "GET",
            "function": self.hello
        }
    ]


    def token_required(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            app = args[0]
            token = None
            if 'token' in app.event.get('http', {}).get('headers', {}):
                token = True
            if not token:
                if "text/html" in app.event.get('http', {}).get('headers', {}).get("accept", ""):
                    return {"status": 401, "response": "Valid credentials required."}
                else:
                    return {"status": 401, "response": {"message": "Valid credentials required."}}
            app.current_user = "Michael"
            return f(*args, **kwargs)
        return decorator


    def index(self, *args, **kwargs):
        return {
            "status": 200,
            "response": self.event
        }


    @token_required
    def hello(self, *args, **kwargs):
        greeting = {"greeting": f"hello {self.current_user}!"}
        return {
            "status": 200,
            "response": greeting
        }


def main(event, context):
    app = WebApp(event)

    info = event.get("http", {})
    path = info.get("path", "")
    method = info.get("method", "GET")

    req = {
        "path": path,
        "method": method
    }


    status = 200
    data = None
    for route in app.routes:
        if req['path'] == route['path'] and req['method'] == route['method']:
            data = route['function']()
    if data:
        status = data['status']
        response = data['response']
    else:
        status = 404
        response = None
    
    return {
        "statusCode": status,
        "body": response
    }