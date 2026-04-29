from __future__ import annotations

import logging
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from epub_generator.config import SourceConfig
from epub_generator.ingestors.url_ingestor import UrlIngestor


class MockResponse:
    def __init__(self, text: str, status_code: int = 200) -> None:
        self.text = text
        self.status_code = status_code

    def raise_for_status(self) -> None:
        import requests
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP Error {self.status_code}")


@pytest.fixture
def ingestor() -> UrlIngestor:
    return UrlIngestor()


def test_url_ingestor_basic(ingestor: UrlIngestor, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    html = """
    <html>
        <body>
            <header>No</header>
            <script>console.log("no")</script>
            <h1>Titulo Real</h1>
            <p>Contenido.</p>
            <img src="http://example.com/img.png" />
            <footer>No</footer>
        </body>
    </html>
    """
    
    def mock_get(*args, **kwargs):
        return MockResponse(html)
        
    import requests
    monkeypatch.setattr(requests, "get", mock_get)
    
    source = SourceConfig(type="url", url="http://example.com")
    md = ingestor.extract(source, tmp_path)
    
    assert "Titulo Real" in md
    assert "Contenido." in md
    assert "console.log" not in md
    assert "No" not in md
    assert "[Ver imagen en la fuente original](http://example.com/img.png)" in md


def test_url_ingestor_with_selector(ingestor: UrlIngestor, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    html = """
    <html><body>
        <div id="ignore">Ignorar</div>
        <article>
            <p>Contenido principal</p>
        </article>
    </body></html>
    """
    monkeypatch.setattr("requests.get", lambda *a, **kw: MockResponse(html))
    
    source = SourceConfig(type="url", url="http://example.com", selector="article")
    md = ingestor.extract(source, tmp_path)
    
    assert "Contenido principal" in md
    assert "Ignorar" not in md


def test_url_ingestor_timeout_skip(ingestor: UrlIngestor, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    def mock_get_fail(*args, **kwargs):
        import requests
        raise requests.Timeout("Timeout!")
        
    monkeypatch.setattr("requests.get", mock_get_fail)
    
    source = SourceConfig(type="url", url="http://example.com", on_error="skip")
    with caplog.at_level(logging.WARNING):
        md = ingestor.extract(source, tmp_path)
        
    assert md == ""
    assert "No se pudo descargar http://example.com" in caplog.text


def test_url_ingestor_timeout_abort(ingestor: UrlIngestor, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    def mock_get_fail(*args, **kwargs):
        import requests
        raise requests.Timeout("Timeout!")
        
    monkeypatch.setattr("requests.get", mock_get_fail)
    
    source = SourceConfig(type="url", url="http://example.com", on_error="abort")
    
    with pytest.raises(RuntimeError, match="Error al descargar"):
        ingestor.extract(source, tmp_path)


def test_url_ingestor_relative_links(ingestor: UrlIngestor, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    html = '<html><body><a href="/docs/guide.html">Guia</a><img src="/img/logo.png"/></body></html>'
    monkeypatch.setattr("requests.get", lambda *a, **kw: MockResponse(html))
    
    source = SourceConfig(type="url", url="https://example.com/path/")
    md = ingestor.extract(source, tmp_path)
    
    assert "(https://example.com/docs/guide.html)" in md
    assert "(https://example.com/img/logo.png)" in md


def test_url_ingestor_registered() -> None:
    from epub_generator.ingestors import INGESTORS
    assert "url" in INGESTORS
    assert INGESTORS["url"] is UrlIngestor
