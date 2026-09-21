#!/usr/bin/env python3
"""Dependency-free quality checks for the static portfolio."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_URL = "https://andminin-engineering.github.io/portfolio.andminin.biz/"
FORBIDDEN_COPY = ("placeholder", "pending integration", "lorem ipsum")


class PortfolioParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.has_main = False
        self.has_h1 = False
        self.has_description = False
        self.has_canonical = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if element_id := attributes.get("id"):
            self.ids.append(element_id)
        if tag == "main":
            self.has_main = True
        if tag == "h1":
            self.has_h1 = True
        if tag == "meta" and attributes.get("name") == "description" and attributes.get("content"):
            self.has_description = True
        if tag == "link" and attributes.get("rel") == "canonical":
            self.has_canonical = attributes.get("href") == EXPECTED_URL
        for attribute in ("href", "src"):
            if value := attributes.get(attribute):
                self.links.append((attribute, value))


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_html(errors: list[str]) -> None:
    html_path = ROOT / "index.html"
    html = html_path.read_text(encoding="utf-8")
    parser = PortfolioParser()
    parser.feed(html)

    if len(parser.ids) != len(set(parser.ids)):
        fail("index.html contains duplicate IDs", errors)
    if not parser.has_main or not parser.has_h1:
        fail("index.html must contain one main landmark and an h1", errors)
    if not parser.has_description or not parser.has_canonical:
        fail("index.html is missing the expected description or canonical URL", errors)

    ids = set(parser.ids)
    for attribute, value in parser.links:
        if value.startswith("#"):
            if value[1:] not in ids:
                fail(f"Broken page anchor: {value}", errors)
            continue
        if value.startswith(("https://", "mailto:")):
            continue
        path = (ROOT / value.split("#", 1)[0]).resolve()
        if ROOT not in path.parents and path != ROOT:
            fail(f"Local {attribute} escapes repository root: {value}", errors)
        elif not path.exists():
            fail(f"Missing local {attribute}: {value}", errors)

    lowered = html.lower()
    for forbidden in FORBIDDEN_COPY:
        if forbidden in lowered:
            fail(f"Public copy contains forbidden marker: {forbidden}", errors)


def validate_public_files(errors: list[str]) -> None:
    sitemap_path = ROOT / "sitemap.xml"
    ET.parse(sitemap_path)
    if EXPECTED_URL not in sitemap_path.read_text(encoding="utf-8"):
        fail("sitemap.xml does not contain the canonical URL", errors)
    if EXPECTED_URL + "sitemap.xml" not in (ROOT / "robots.txt").read_text(encoding="utf-8"):
        fail("robots.txt does not reference the public sitemap", errors)


def main() -> int:
    errors: list[str] = []
    validate_html(errors)
    validate_public_files(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Portfolio validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
