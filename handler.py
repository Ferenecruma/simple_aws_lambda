import json
import requests


def measure_response_time(url: str) -> str:
    """Make request to the url and returns time elapsed before response."""
    try:
        response = requests.get(url)
        return response.elapsed.total_seconds()
    except Exception as ex:
        return f"While making request following exception has occured: {repr(ex)}"


def main(event, context):
    try:
        request_body = json.loads(event["body"])
    except KeyError:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Cannot get request's body."}),
        }
        
    try:
        url_for_request = request_body["url"]
    except KeyError:
        response = {
            "statusCode": 404,
            "body": json.dumps(
                {
                    "message": "url for the measurement is not provided!",
                }
            ),
        }
    else:
        response = {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Results from response time measurement.",
                    "result": measure_response_time(url_for_request),
                }
            ),
        }

    return response
