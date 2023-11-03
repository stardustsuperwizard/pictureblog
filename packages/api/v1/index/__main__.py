import logging


def main(event, context):
    status = 200
    return {
        "statusCode": status,
        "body": event
    }

