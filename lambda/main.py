import os
import boto3


def handler(event, context):
    # Raw event data
    path = event["rowPath"]
    if path != "/":
        return {"statusCode": 404, "body": "Not Found"}

    # Get the table name from the environment variable
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.getenv("TABLE_NAME"))

    # Read the visit count from the DynamoDB table (or initialize it if it doesn't exist)
    response = table.get_item(Key={"key": "visit_count"})
    if "Item" in response:
        visit_count = response["Item"]["value"]
    else:
        visit_count = 0

    # Increment the visit count and write it back to the table
    new_visit_count = visit_count + 1
    table.put_item(Item={"key": "visit_count", "value": new_visit_count})

    version = os.getenv("VERSION", "0.0")
    response_body = {
        "message": "Hello, World from Lambda! 🚀 ",
        "version": version,
        "visit_count": new_visit_count,
    }
    return {"statusCode": 200, "body": response_body}
