import ipaddress
import json
from urllib.parse import urlparse

import httpx

from mindee.error.mindee_error import MindeeSourceError
from mindee.parsing.common.string_dict import StringDict

_CGNAT_BLOCK = ipaddress.IPv4Network("100.64.0.0/10")
_IPV6_UNIQUE_LOCAL = ipaddress.IPv6Network("fc00::/7")


def validate_url_for_source(url: str) -> None:
    """
    Validates that a URL is safe to send to the Mindee server.

    Rejects any URL that could be used for Server-Side Request Forgery (SSRF):

    - non-HTTPS schemes,
    - embedded userinfo (e.g. ``https://user:pass@host``),
    - loopback hostnames (``localhost``, ``*.localhost``),
    - literal IP addresses that are loopback, link-local, private (RFC 1918),
      any-local (``0.0.0.0``), multicast, IPv6 unique-local (``fc00::/7``),
      or carrier-grade NAT (``100.64.0.0/10``).

    Note: DNS resolution is not performed. A hostname that resolves to a
    private IP will not be caught here.

    :param url: The URL string to validate.
    :raises MindeeSourceError: If the URL fails any security check.
    """
    try:
        parsed = urlparse(url)
    except Exception as exc:
        raise MindeeSourceError("Invalid URL") from exc

    if parsed.scheme.lower() != "https":
        raise MindeeSourceError("URL must be HTTPS")

    if parsed.username or parsed.password:
        raise MindeeSourceError("Source URLs must not embed user credentials")

    host = parsed.hostname
    if not host:
        raise MindeeSourceError("Source URL is missing a host")

    lower_host = host.lower()
    if (
        lower_host == "localhost"
        or lower_host.endswith(".localhost")
        or lower_host == "ip6-localhost"
        or lower_host == "ip6-loopback"
    ):
        raise MindeeSourceError(f"Loopback hostnames are not allowed: {host}")

    try:
        addr = ipaddress.ip_address(lower_host)
    except ValueError:
        return

    if (
        addr.is_loopback
        or addr.is_link_local
        or addr.is_private
        or addr.is_unspecified
        or addr.is_multicast
    ):
        raise MindeeSourceError(f"URL host resolves to a disallowed address: {addr}")

    if isinstance(addr, ipaddress.IPv4Address) and addr in _CGNAT_BLOCK:
        raise MindeeSourceError(f"URL host resolves to a disallowed address: {addr}")

    if isinstance(addr, ipaddress.IPv6Address) and addr in _IPV6_UNIQUE_LOCAL:
        raise MindeeSourceError(f"URL host resolves to a disallowed address: {addr}")


def is_valid_sync_response(response: httpx.Response) -> bool:
    """
    Checks if the synchronous response is valid. Returns True if the response is valid.

    :param response: a requests response object.
    :return: bool
    """
    if not response or response.is_error:
        return False
    try:
        response_json = response.json()
    except httpx.DecodingError:
        return False
    # EXTREMELY rare edge case where raw html is sent instead of json.
    return isinstance(response_json, dict)


def is_valid_async_response(response: httpx.Response) -> bool:
    """
    Checks if the asynchronous response is valid. Also checks if it is a valid synchronous response.

    Returns True if the response is valid.

    :param response: an httpx response object.
    :return: bool
    """
    if not is_valid_sync_response(response):
        return False
    response_json = json.loads(response.content)
    # Checks invalid status codes within the bounds of ok responses.
    if response.status_code and (
        response.status_code < 200 or response.status_code > 302
    ):
        return False
    if "job" in response_json:
        return not response_json["job"].get("error")
    if "execution" in response_json:
        return not response_json["execution"].get("error")
    return False


def clean_request_json(response: httpx.Response) -> StringDict:
    """
    Checks and correct the response error format depending on the two possible kind of returns.

    :param response: Raw request response.
    :return: Returns the job error if the error is due to parsing, returns the http error otherwise.
    """
    response_json = response.json()
    if response.is_error:
        response_json["status_code"] = response.status_code
        return response_json
    corrected_json = response_json
    if (
        "api_request" in response_json
        and "status_code" in response_json["api_request"]
        and isinstance(response_json["api_request"]["status_code"], (int, str))
        and str(response_json["api_request"]["status_code"]).isdigit()
        and int(response_json["api_request"]["status_code"]) >= 400
    ):
        corrected_json["status_code"] = int(response_json["api_request"]["status_code"])
    if (
        "job" in response_json
        and "error" in response_json["job"]
        and response_json["job"]["error"]
    ):
        corrected_json["error"] = response_json["job"]["error"]
        corrected_json["status_code"] = 500
    return corrected_json
