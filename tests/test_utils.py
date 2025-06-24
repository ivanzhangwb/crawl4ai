import pytest
from crawl4ai.utils import normalize_url, normalize_url_for_deep_crawl


def test_normalize_url_basic():
    base = "https://docs.example.com/platform/release-notes/"
    # Relative up two levels
    assert normalize_url("../../getting-started/tutorials/build-code-tool/", base) == "https://docs.example.com/getting-started/tutorials/build-code-tool/"
    # Relative up one level
    assert normalize_url("../foo/", base) == "https://docs.example.com/platform/foo/"
    # Root relative
    assert normalize_url("/absolute/path/", base) == "https://docs.example.com/absolute/path/"
    # Absolute URL
    assert normalize_url("https://other.com/page", base) == "https://other.com/page"
    # Anchor
    assert normalize_url("#section1", base) == "https://docs.example.com/platform/release-notes/#section1"
    # Same directory
    assert normalize_url("file.html", base) == "https://docs.example.com/platform/release-notes/file.html"
    # Protocol-relative
    assert normalize_url("//cdn.com/lib.js", base) == "https://cdn.com/lib.js"


def test_normalize_url_for_deep_crawl():
    base = "https://docs.example.com/platform/release-notes/"
    # Remove tracking params, fragment, lowercase host
    url = "../../getting-started/tutorials/build-code-tool/?utm_source=foo&utm_campaign=bar#frag"
    result = normalize_url_for_deep_crawl(url, base)
    assert result == "https://docs.example.com/getting-started/tutorials/build-code-tool"
    # Query params kept if not tracking
    url2 = "../foo/?q=1"
    result2 = normalize_url_for_deep_crawl(url2, base)
    assert result2 == "https://docs.example.com/platform/foo?q=1"
    # Absolute
    url3 = "https://Other.com/abc/?ref=123#frag"
    result3 = normalize_url_for_deep_crawl(url3, base)
    assert result3 == "https://other.com/abc" 