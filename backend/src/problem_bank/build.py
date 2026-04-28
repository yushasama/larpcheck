#!/usr/bin/env python3
"""
build.py - Compile problem JSONs into styled HTML files.

Usage:
    python build.py                     # build all problems/
    python build.py a b e               # build specific problems by id
    python build.py --out ./dist        # write to custom output dir
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "ransomware"))

# These pages get bundled as standalone HTML, so the CSS lives inline here.

BADGE_STYLES = {
    "hard": ("background:#fce4ef;color:#993556;", "Hard"),
    "topic": ("background:#f0eaff;color:#5c3a9e;", None),  # label from JSON
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@700&family=M+PLUS+1p:wght@400;500;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
html,body{background:#fff;color:#1a0a1e;}
body{font-family:'M PLUS 1p',sans-serif;}
.shell{max-width:720px;margin:0 auto;padding:32px 24px 60px;}
.prob-title{font-family:'Noto Serif JP',serif;font-size:24px;font-weight:700;color:#1a0a1e;margin-bottom:8px;line-height:1.3;border-bottom:1.5px solid #f0d6e8;padding-bottom:20px;}
.prob-meta{display:flex;gap:12px;margin-bottom:20px;margin-top:12px;}
.badge{font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:3px 10px;border-radius:20px;}
.section-label{font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#e84f8a;margin-bottom:10px;margin-top:24px;}
.stmt{font-size:14px;line-height:1.9;color:#2a1a2e;margin-bottom:28px;}
.stmt p{margin-bottom:12px;}
.stmt p:last-child{margin-bottom:0;}
.constraints{margin-bottom:28px;}
.constraint-row{padding:7px 0;border-bottom:1px solid #f5eaf0;font-size:14px;color:#2a1a2e;}
.constraint-row:last-child{border-bottom:none;}
.c-sym{color:#7b5cba;font-weight:700;font-family:monospace;font-size:13px;}
.note{background:#fffbea;border-left:3px solid #c9a227;padding:10px 14px;border-radius:0 6px 6px 0;font-size:13px;color:#5d4000;line-height:1.6;margin-bottom:16px;}
.samples{display:flex;flex-direction:column;gap:16px;}
.sample{border:1px solid #f0d6e8;border-radius:10px;overflow:hidden;}
.sample-head{background:#fce4ef;padding:8px 14px;font-size:11px;font-weight:700;color:#993556;letter-spacing:0.07em;text-transform:uppercase;}
.sample-body{display:grid;grid-template-columns:1fr 1fr;}
.sample-col{padding:12px 14px;}
.sample-col:first-child{border-right:1px solid #f0d6e8;}
.sample-col-label{font-size:11px;color:#8a6a7a;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:6px;}
.sample-code{font-family:monospace;font-size:13px;line-height:1.7;color:#1a0a1e;white-space:pre;}
""".strip()

# Small helpers keep the HTML assembly below from turning into one giant string.

def render_paragraphs(paragraphs: list[str], css_class: str = "stmt") -> str:
    inner = "\n".join(f"  <p>{p}</p>" for p in paragraphs)

    return f'<div class="{css_class}">\n{inner}\n</div>'


def render_constraints(constraints: list[str]) -> str:
    rows = "\n".join(
        f'  <div class="constraint-row"><span class="c-sym">{c}</span></div>'
        for c in constraints
    )

    return f'<div class="constraints">\n{rows}\n</div>'


def render_badges(badges: list[dict]) -> str:
    if not badges:
        return ""

    items = []

    for badge in badges:
        style, default_label = BADGE_STYLES.get(badge["type"], ("", None))
        label = badge.get("label") or default_label or badge["type"]
        items.append(f'<span class="badge" style="{style}">{label}</span>')

    badges_html = "\n  ".join(items)

    return f'<div class="prob-meta">\n  {badges_html}\n</div>'


def render_notes(notes: list[str]) -> str:
    return "\n".join(f'<div class="note">{note}</div>' for note in notes)


def render_samples(samples: list[dict]) -> str:
    blocks = []

    for sample in samples:
        sample_html = f"""<div class="sample">
  <div class="sample-head">{sample['label']}</div>
  <div class="sample-body">
    <div class="sample-col">
      <div class="sample-col-label">Input</div>
      <div class="sample-code">{sample['input']}</div>
    </div>
    <div class="sample-col">
      <div class="sample-col-label">Output</div>
      <div class="sample-code">{sample['output']}</div>
    </div>
  </div>
</div>"""
        blocks.append(sample_html)

    return '<div class="samples">\n' + "\n".join(blocks) + "\n</div>"


def render_section(label: str, content: str) -> str:
    return f'<div class="section-label">{label}</div>\n{content}'


def build_problem(json_path: Path, out_dir: Path) -> None:
    data = json.loads(json_path.read_text())

    # Keeping sections separate makes the final HTML much easier to tweak.
    parts = [
        f"<style>\n{CSS}\n</style>",
        '<div class="shell">',
        f'  <div class="prob-title">{data["title"]}</div>',
    ]

    if data.get("badges"):
        parts.append(render_badges(data["badges"]))

    parts.append(render_section("Statement", render_paragraphs(data["statement"])))
    parts.append(render_section("Input", render_paragraphs(data["input_format"])))
    parts.append(render_section("Output", render_paragraphs(data["output_format"])))
    parts.append(render_section("Constraints", render_constraints(data["constraints"])))

    pre_notes = data.get("notes", [])
    if pre_notes:
        parts.append(render_section("Notes", render_notes(pre_notes)))

    parts.append(render_section("Sample I/O", render_samples(data["samples"])))
    parts.append("</div>")

    html = "\n\n".join(parts)
    out_path = out_dir / f"{data['id']}.html"
    out_path.write_text(html)

    print(f"  built -> {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build problem HTMLs from JSONs.")
    parser.add_argument("ids", nargs="*", help="Problem IDs to build (default: all)")
    parser.add_argument("--src", default="../problem_bank", help="Source JSON directory")
    parser.add_argument("--out", default="../ransomware/resources/problems", help="Output HTML directory")

    args = parser.parse_args()

    src_dir = Path(args.src)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.ids:
        json_paths = [src_dir / f"{pid}.json" for pid in args.ids]
        missing = [path for path in json_paths if not path.exists()]
        if missing:
            print(f"ERROR: missing JSON files: {[str(path) for path in missing]}", file=sys.stderr)
            sys.exit(1)
    else:
        json_paths = sorted(src_dir.glob("*.json"))

    if not json_paths:
        print("No JSON files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Building {len(json_paths)} problem(s)...")

    for path in json_paths:
        build_problem(path, out_dir)

    print("Done.")


if __name__ == "__main__":
    main()
