import asyncio
from urllib.parse import urlparse


async def ping(rtsp: str, timeout: int = 3) -> bool:
    """Asynchronously ping the camera to check its availability."""
    parsed_url = urlparse(rtsp)
    if parsed_url.scheme not in ('rtsp', 'rtsps'):
        return False

    ip, port = parsed_url.hostname, parsed_url.port or 554

    try:
        _, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=timeout)
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False
    else:
        writer.close()
        await writer.wait_closed()
        return True
