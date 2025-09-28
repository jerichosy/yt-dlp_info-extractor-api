import pytest

from main import extract_media_info


@pytest.mark.parametrize(
    "url",
    [
        # "https://www.instagram.com/reel/C-RJokDy9xd",
        "https://www.instagram.com/reel/DPFk1TBj2-O",
        "https://www.instagram.com/p/DAFJPYCvkQw",
        "https://www.facebook.com/reel/307664589035540",
    ],
)
def test_extract_media_info_returns_metadata(url: str) -> None:
    media_info = extract_media_info(url)

    assert isinstance(media_info, dict)
    assert media_info, "yt-dlp returned an empty metadata dictionary"
    assert media_info.get("id"), "yt-dlp metadata is missing the media id"
    assert media_info.get("formats"), "yt-dlp metadata is missing or has an empty 'formats' array"
