"""Validate the entire batch, then replace only generated contribution images.

No file is published if any expected source is missing or is not an SVG.
GitHub Actions commits only after this program succeeds.
"""
from pathlib import Path
import os
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "snake-light.svg": ".profile-build/snake-light.svg",
    "snake-dark.svg": ".profile-build/snake-dark.svg",
    "city-light.svg": "profile-3d-contrib/profile-season-animate.svg",
    "city-dark.svg": "profile-3d-contrib/profile-night-rainbow.svg",
}


def publish(root=ROOT):
    batch = {}
    for target, source in SOURCES.items():
        data = (root / source).read_bytes()
        element = ET.fromstring(data)
        if element.tag != "{http://www.w3.org/2000/svg}svg":
            raise ValueError(f"Not an SVG: {source}")
        if b"<script" in data.lower() or not (element.get("viewBox") or (element.get("width") and element.get("height"))):
            raise ValueError(f"Invalid SVG content or dimensions: {source}")
        batch[target] = data
    output = root / "assets" / "generated"
    output.mkdir(parents=True, exist_ok=True)
    for target, data in batch.items():
        temporary = output / (target + ".tmp")
        temporary.write_bytes(data)
        os.replace(temporary, output / target)
    print("Validated and published four contribution SVGs.")


if __name__ == "__main__":
    publish()
