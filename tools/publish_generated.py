"""Validate the entire batch, then replace only generated contribution images.

No file is published if any expected source is missing or is not an SVG.
GitHub Actions commits only after this program succeeds.
"""
from pathlib import Path
import os
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "snake-light.svg": ".profile-build/snake-light.svg",
    "snake-dark.svg": ".profile-build/snake-dark.svg",
    "city-light.svg": "profile-3d-contrib/profile-season-animate.svg",
    "city-dark.svg": "profile-3d-contrib/profile-night-rainbow.svg",
}


def simplify_city(data):
    """Remove sparse PR/issue radar and keep the city, languages and contributions."""
    root = ET.fromstring(data)
    children = list(root)
    changed = False
    radar = next((group for group in children if any(
        node.tag == f"{{{SVG_NS}}}text" and (node.text or "").strip() == "Issue"
        for node in group.iter()
    )), None)
    if radar is not None:
        root.remove(radar)
        changed = True

    languages = next((group for group in root if any(
        node.tag == f"{{{SVG_NS}}}title" and (node.text or "").startswith("Java ")
        for node in group.iter()
    )), None)
    if languages is not None and languages.get("transform") != "translate(800, 100)":
        languages.set("transform", "translate(800, 100)")
        changed = True

    summary = next((group for group in root if any(
        node.tag == f"{{{SVG_NS}}}text" and (node.text or "").strip() == "contributions"
        for node in group
    )), None)
    if summary is not None:
        texts = [node for node in summary if node.tag == f"{{{SVG_NS}}}text"]
        count = next((node for node in texts if (node.text or "").strip().isdigit()), None)
        label = next((node for node in texts if (node.text or "").strip() == "contributions"), None)
        date = next((node for node in texts if "/" in (node.text or "")), None)
        for node in list(summary):
            if node not in (count, label, date):
                summary.remove(node)
                changed = True
        if count is not None:
            if count.get("x") != "610":
                count.set("x", "610")
                changed = True
        if label is not None:
            if label.get("x") != "620":
                label.set("x", "620")
                changed = True

    return ET.tostring(root, encoding="utf-8", xml_declaration=True) if changed else data


def publish(root=ROOT):
    batch = {}
    for target, source in SOURCES.items():
        data = (root / source).read_bytes()
        element = ET.fromstring(data)
        if element.tag != "{http://www.w3.org/2000/svg}svg":
            raise ValueError(f"Not an SVG: {source}")
        if b"<script" in data.lower() or not (element.get("viewBox") or (element.get("width") and element.get("height"))):
            raise ValueError(f"Invalid SVG content or dimensions: {source}")
        batch[target] = simplify_city(data) if target.startswith("city-") else data
    output = root / "assets" / "generated"
    output.mkdir(parents=True, exist_ok=True)
    for target, data in batch.items():
        temporary = output / (target + ".tmp")
        temporary.write_bytes(data)
        os.replace(temporary, output / target)
    print("Validated and published four contribution SVGs.")


if __name__ == "__main__":
    publish()
