"""Deterministic service regressions; no requests to third-party media sites."""
import asyncio
from unittest.mock import MagicMock, patch
import pytest
from fastapi import HTTPException, Response
import main

def test_root():
    assert asyncio.run(main.root()) == {'message': 'Hello, World!'}

def test_extraction_uses_metadata_only_and_sanitizes():
    with patch.object(main.yt_dlp, 'YoutubeDL') as factory:
        downloader = factory.return_value.__enter__.return_value
        downloader.extract_info.return_value = {'id': 'test-id'}
        downloader.sanitize_info.return_value = {'id': 'test-id', 'formats': []}
        assert main.extract_media_info('https://example.invalid/video') == {'id': 'test-id', 'formats': []}
        downloader.extract_info.assert_called_once_with('https://example.invalid/video', download=False)
        downloader.sanitize_info.assert_called_once_with({'id': 'test-id'})

def test_extract_success_sets_installed_version_header():
    response = Response()
    with patch.object(main, 'extract_media_info', return_value={'id': 'test-id'}):
        assert main.extract('https://example.invalid/video', response) == {'id': 'test-id'}
    assert response.headers[main.HEADER_NAME_YT_DLP_VER] == main.yt_dlp.version.__version__

def test_extract_failure_preserves_status_detail_and_version():
    with patch.object(main, 'extract_media_info', side_effect=RuntimeError('test extraction failure')):
        with pytest.raises(HTTPException) as error:
            main.extract('https://example.invalid/video', Response())
    assert error.value.status_code == 500
    assert error.value.detail == 'test extraction failure'
    assert error.value.headers[main.HEADER_NAME_YT_DLP_VER] == main.yt_dlp.version.__version__

def test_reserved_route():
    with pytest.raises(HTTPException) as error:
        asyncio.run(main.stop_generating())
    assert error.value.status_code == 501

def test_openapi_exposes_routes():
    paths = main.app.openapi()['paths']
    assert '/extract' in paths and 'get' in paths['/extract']
    assert '/waikei-pretrained/stop-generating' in paths
