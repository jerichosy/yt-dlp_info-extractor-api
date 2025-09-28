import asyncio

import yt_dlp
from fastapi import APIRouter, FastAPI, HTTPException, Response

app = FastAPI()


# Despite the official recommendation to not prefix custom proprietary headers with "X-", keep using so as our use case is private and not a standard.
HEADER_NAME_YT_DLP_VER = "X-YT-DLP-Ver"


def _yt_dlp_version() -> str:
    return yt_dlp.version.__version__


def extract_media_info(url: str) -> dict:
    """Fetch metadata for a given URL using yt-dlp without downloading the media."""
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return ydl.sanitize_info(info_dict)


@app.get("/")
async def root(timeout: int = None):
    if timeout:
        # Yes, we can use time.sleep() instead, but acdg. to FastAPI docs: https://stackoverflow.com/a/75470289,
        # `def` functions are "run in an external threadpool that is then awaited, instead of being called directly (as it would block the server)."
        # Remember that this is an ASGI server, that's why there's practically no difference between `time.sleep()` and `asyncio.sleep()`.
        # But technically, `asyncio.sleep()` is more efficient since threading have more overhead.
        await asyncio.sleep(timeout)
    return {"message": "Hello, World!"}

@app.get("/extract")
def extract(url: str, response: Response):
    yt_dlp_version = _yt_dlp_version()
    response.headers[HEADER_NAME_YT_DLP_VER] = yt_dlp_version  # ! WARNING: Do not do this in widely used web apps as versions can indicate security vulnerabilities.

    try:
        return extract_media_info(url)
    except Exception as e:
        error_message = str(e)
        raise HTTPException(status_code=500, detail=error_message, headers={HEADER_NAME_YT_DLP_VER: yt_dlp_version})  # Include header as it is not in here by default.

waikei_llm_router = APIRouter()

@waikei_llm_router.post("/stop-generating")
async def stop_generating():
    # Raise 501 instead of 405 since this is a server-side issue, not client's.
    raise HTTPException(status_code=501, detail="Method has not been implemented")

app.include_router(waikei_llm_router, prefix="/waikei-pretrained", tags=["waikei-llm"])
