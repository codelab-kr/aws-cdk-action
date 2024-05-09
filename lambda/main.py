import os


def handler(event, context):
    version = os.getenv("VERSION", "0.0")
    response_body = {
        "message": "Hello, World from Lambda! 🚀 ",
        "version": version,
    }
    return {"statusCode": 200, "body": response_body}
