import asyncio
import json

from aiohttp import ClientSession, ClientTimeout
from dacite import from_dict
from hydrogram.types import Message

from bot.config import CONTENT_API
from bot.schemas.download import CommonLinks
from bot.schemas.telegram import ResponseUtility
from bot.telegram.parsing import parse_attributes

REQUEST_TIMEOUT = ClientTimeout(total=120)
MAX_ATTEMPTS = 3


class ContentAPIError(RuntimeError):
    """Raised when the Content API reports a failure or returns no media."""


def _error_message(payload: object, status: int) -> str:
    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, dict) and error.get("message"):
            return str(error["message"])
    return f"Content API returned HTTP {status}"


async def get_api_result(endpoint: str, m: Message) -> ResponseUtility:
    attrs = parse_attributes(m)
    api_url = f"{CONTENT_API.rstrip('/')}/{endpoint}"
    last_error: Exception | None = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            async with ClientSession(timeout=REQUEST_TIMEOUT) as session:
                async with session.get(api_url, params={"url": attrs.url}) as response:
                    status = response.status
                    body = await response.text()

            try:
                payload = json.loads(body)
            except json.JSONDecodeError as error:
                raise ContentAPIError(
                    f"Content API returned non-JSON (HTTP {status}, {len(body)} bytes)"
                ) from error

            if status != 200 or not isinstance(payload, dict):
                raise ContentAPIError(_error_message(payload, status))
            if not payload.get("success"):
                raise ContentAPIError(_error_message(payload, response.status))

            result = from_dict(data_class=CommonLinks, data=payload)
            if not result.media:
                raise ContentAPIError("Content API returned no media")

            return ResponseUtility(
                result=result,
                button=attrs.button,
                caption=attrs.caption,
            )
        except Exception as error:
            last_error = error
            if attempt < MAX_ATTEMPTS:
                await asyncio.sleep(0.5 * attempt)

    raise ContentAPIError(f"Content API call failed after {MAX_ATTEMPTS} attempts: {last_error}")
