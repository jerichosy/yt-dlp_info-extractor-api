import asyncio

import yt_dlp
from fastapi import APIRouter, FastAPI, HTTPException

app = FastAPI()


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
def extract(url: str):
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return ydl.sanitize_info(info_dict)
    except Exception as e:
        error_message = str(e)
        raise HTTPException(status_code=500, detail=error_message)

waikei_llm_router = APIRouter()

@waikei_llm_router.get("/stop-generating")
async def stop_generating():
    # return {"message": "Method has not been implemented"}
    raise HTTPException(status_code=501, detail="Method has not been implemented")

app.include_router(waikei_llm_router, prefix="/waikei-pretrained", tags=["waikei-llm"])
