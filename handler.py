import time
import asyncio
import json
from typing import Dict
import aiohttp
import logging
from aiohttp import ClientSession


FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('tcpserver')


async def set_responses_time(websites: Dict[str, str]) -> None:
    """Set response time for the given websites."""
    async with ClientSession() as session:
        tasks = []
        for title, url in websites.items():
            tasks.append(measure_response_time(title, url, websites, session))
        await asyncio.gather(*tasks)


async def measure_response_time(
    title: str, url: str, websites: dict, session: ClientSession
) -> None:
    """Set the response time for the url given."""
    request_start = time.monotonic()
    try:
        await session.get(url)
    except Exception as ex:
        logger.error(f'Following error occured while making requst to the {url}, {ex}')
        response_time = "Couldn't measure response time for the given website."
    else:
        response_time = time.monotonic() - request_start

    websites[title] = response_time


def main(event, context):
    try:
        websites = json.loads(event["body"])
    except KeyError:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Cannot get request's body."}),
        }

    if isinstance(websites, dict):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(set_responses_time(websites))

        response = {
            "statusCode": 200,
            "body": json.dumps(websites),
        }
    else:
        response = {
            "statusCode": 404,
            "body": json.dumps(
                {
                    "message": "Request's body is not valid!It should be dictionary.",
                }
            ),
        }

    return response
