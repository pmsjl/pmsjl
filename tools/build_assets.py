"""Build self-contained profile SVGs; optionally seed honest first-run placeholders.

Usage: python tools/build_assets.py [--seed-placeholders]
Only generated placeholder files that do not yet exist are seeded.
"""
from pathlib import Path
import argparse
import xml.etree.ElementTree as ET

ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Microsoft YaHei',sans-serif"


def svg(name, width, height, content, css=""):
    data = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
<style>text{{font-family:{FONT}}}{css}</style>
{content}
</svg>\n'''
    (ASSETS / name).write_text(data, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-placeholders", action="store_true")
    args = parser.parse_args()
    ASSETS.mkdir(parents=True, exist_ok=True)
    defs = '''<defs>
<linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0F172A"/><stop offset=".58" stop-color="#172554"/><stop offset="1" stop-color="#35215e"/></linearGradient>
<linearGradient id="line"><stop stop-color="#3B82F6"/><stop offset=".55" stop-color="#8B5CF6"/><stop offset="1" stop-color="#38BDF8"/></linearGradient>
<radialGradient id="glow"><stop stop-color="#8B5CF6" stop-opacity=".3"/><stop offset="1" stop-color="#8B5CF6" stop-opacity="0"/></radialGradient>
</defs>'''
    # Generated with the same services and parameters as the user's reference.
    # Keep the original waving/typing structure and embedded Fira Code font.
    ns = "{http://www.w3.org/2000/svg}"
    for name in ("hero", "typing"):
        tree = ET.fromstring((ROOT / "tools/templates" / f"{name}.svg").read_text(encoding="utf-8"))
        style = tree.find(ns + "style")
        if name == "hero":
            style.text += "\n.desc{font-weight:700}"
        else:
            style.text += "\ntext{font-weight:600}"
        reduced_rules = []
        for index, parent in enumerate(tree.iter()):
            for animation in list(parent):
                if animation.tag != ns + "animate":
                    continue
                attribute = animation.get("attributeName")
                value = animation.get("values", "").split(";")[0].strip()
                if name == "typing":
                    value = "m0,50 h800" if parent.get("id") == "path0" else "m0,50 h0"
                parent.set("id", parent.get("id", f"wave-{index}"))
                if attribute == "d":
                    reduced_rules.append(f"#{parent.get('id')}{{d:path('{value}')}}")
        style.text += "\n@media(prefers-reduced-motion:reduce){*{animation:none!important}" + "".join(reduced_rules) + "}"
        ET.ElementTree(tree).write(ASSETS / f"{name}.svg", encoding="unicode")
        for parent in tree.iter():
            for animation in list(parent):
                if animation.tag != ns + "animate":
                    continue
                attribute = animation.get("attributeName")
                value = animation.get("values", "").split(";")[0].strip()
                if name == "typing":
                    value = "m0,50 h800" if parent.get("id") == "path0" else "m0,50 h0"
                parent.set(attribute, value)
                parent.remove(animation)
        style.text += "\n*{animation:none!important}"
        ET.ElementTree(tree).write(ASSETS / f"{name}-static.svg", encoding="unicode")

    svg("divider.svg", 880, 28, '''<defs><linearGradient id="trail"><stop stop-color="#3B82F6" stop-opacity="0"/><stop offset=".5" stop-color="#8B5CF6"/><stop offset="1" stop-color="#38BDF8" stop-opacity="0"/></linearGradient></defs>
<path d="M0 14H880" stroke="#8B5CF6" opacity=".18"/><rect class="trail" x="0" y="12" width="220" height="4" rx="2" fill="url(#trail)"/>''', '''.trail{animation:travel 8s ease-in-out infinite alternate}@keyframes travel{to{transform:translateX(660px)}}@media(prefers-reduced-motion:reduce){.trail{animation:none;transform:translateX(330px)}}''')

    svg("footer.svg", 880, 132, defs + '''<rect width="880" height="132" rx="14" fill="url(#bg)"/>
<g class="wave" fill="none" stroke="url(#line)" stroke-width="2" opacity=".8"><path d="M-70 25Q90 -5 260 24T580 20T950 20"/><path d="M-70 34Q100 2 280 35T600 29T950 31" opacity=".45"/></g>
<text x="440" y="80" text-anchor="middle" fill="#e2e8f0" font-size="20" letter-spacing="2">THANKS FOR STOPPING BY</text><text x="440" y="108" text-anchor="middle" fill="#a5b4fc" font-size="13">Junjie Xu · pmsjl</text>''', '''.wave{animation:wave 9s ease-in-out infinite}@keyframes wave{50%{transform:translate(26px,5px)}}@media(prefers-reduced-motion:reduce){.wave{animation:none}}''')

    # Explicit picture fallbacks work even if an image context does not inherit
    # the browser's reduced-motion media setting into its internal stylesheet.
    for asset in ("divider", "footer"):
        source = (ASSETS / f"{asset}.svg").read_text(encoding="utf-8")
        override = "*{animation:none!important}.phrase{opacity:0!important}.p1{opacity:1!important}.reveal{width:610px!important}.cursor{opacity:0!important}"
        source = source.replace("</style>", override + "</style>")
        (ASSETS / f"{asset}-static.svg").write_text(source, encoding="utf-8")
    if args.seed_placeholders:
        (ASSETS / "generated").mkdir(exist_ok=True)
        for kind,height in [("snake",166),("city",254)]:
            for theme in ("dark","light"):
                name=f"generated/{kind}-{theme}.svg"
                if (ASSETS/name).exists():
                    continue
                bg,fg,muted = ("#0F172A","#e2e8f0","#a5b4fc") if theme=="dark" else ("#f1f5f9","#0F172A","#4338ca")
                svg(name,880,height,f'<rect x="1" y="1" width="878" height="{height-2}" rx="12" fill="{bg}" stroke="#8B5CF6" stroke-opacity=".4"/><text x="440" y="{height/2-15}" text-anchor="middle" fill="{fg}" font-size="23">等待首次生成</text><text x="440" y="{height/2+18}" text-anchor="middle" fill="{muted}" font-size="14">pmsjl · 启用 Profile visuals 工作流后显示真实公开贡献</text>')
    print("Built profile SVG assets.")


if __name__ == "__main__":
    main()
